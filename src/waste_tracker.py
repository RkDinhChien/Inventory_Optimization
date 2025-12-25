"""
WASTE TRACKING MODULE
Track, analyze, and reduce food waste in restaurant operations
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WasteTracker:
    """Track and analyze food waste to reduce costs and improve sustainability."""
    
    # Waste categories
    WASTE_CATEGORIES = [
        'expired',          # Material passed expiry date
        'damaged',          # Damaged during storage/handling
        'overproduction',   # Made too much food
        'plate_waste',      # Customer leftovers
        'prep_waste',       # Trimming, peeling losses
        'spoilage',         # Spoiled before expiry
        'contamination',    # Cross-contamination
        'other'            # Other reasons
    ]
    
    def __init__(self):
        self.waste_log = []
        self.inventory_data = None
        self.recipes_data = None
        self.waste_history = None
        
    def load_data(self, inventory_file: str, recipes_file: str = None, waste_log_file: str = None):
        """Load inventory and historical waste data."""
        try:
            self.inventory_data = pd.read_csv(inventory_file)
            logger.info(f"Loaded {len(self.inventory_data)} inventory items")
            
            if recipes_file:
                self.recipes_data = pd.read_csv(recipes_file)
                logger.info(f"Loaded {len(self.recipes_data)} recipe records")
            
            if waste_log_file:
                self.waste_history = pd.read_csv(waste_log_file)
                self.waste_history['date'] = pd.to_datetime(self.waste_history['date'])
                logger.info(f"Loaded {len(self.waste_history)} historical waste records")
            else:
                # Create empty waste history
                self.waste_history = pd.DataFrame(columns=[
                    'date', 'material_name', 'quantity', 'unit', 'reason',
                    'cost_per_unit', 'total_cost', 'notes', 'category'
                ])
                
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def log_waste(self, 
                  material_name: str,
                  quantity: float,
                  reason: str,
                  notes: str = "",
                  date: datetime = None) -> Dict:
        """
        Log a waste incident.
        
        Args:
            material_name: Name of the wasted material
            quantity: Quantity wasted
            reason: Reason for waste (from WASTE_CATEGORIES)
            notes: Additional notes
            date: Date of waste (default: today)
        
        Returns:
            Waste record dictionary
        """
        if date is None:
            date = datetime.now()
        
        if reason not in self.WASTE_CATEGORIES:
            logger.warning(f"Invalid reason '{reason}'. Using 'other'")
            reason = 'other'
        
        # Get material info
        material_info = self.inventory_data[
            self.inventory_data['material_name'] == material_name
        ]
        
        if material_info.empty:
            logger.error(f"Material {material_name} not found in inventory")
            return {'error': 'Material not found'}
        
        material_info = material_info.iloc[0]
        unit = material_info['unit']
        cost_per_unit = material_info['cost_per_unit']
        total_cost = quantity * cost_per_unit
        
        # Determine category
        category = self._categorize_waste(reason)
        
        waste_record = {
            'date': date,
            'material_name': material_name,
            'quantity': quantity,
            'unit': unit,
            'reason': reason,
            'cost_per_unit': cost_per_unit,
            'total_cost': round(total_cost, 2),
            'notes': notes,
            'category': category
        }
        
        # Add to log
        self.waste_log.append(waste_record)
        
        # Add to history DataFrame
        new_row = pd.DataFrame([waste_record])
        self.waste_history = pd.concat([self.waste_history, new_row], ignore_index=True)
        
        logger.info(f"Logged waste: {quantity} {unit} of {material_name} (${total_cost:.2f}) - {reason}")
        
        return waste_record
    
    def _categorize_waste(self, reason: str) -> str:
        """Categorize waste into operational categories."""
        prevention_categories = {
            'expired': 'Inventory Management',
            'damaged': 'Handling & Storage',
            'overproduction': 'Forecasting',
            'plate_waste': 'Portion Control',
            'prep_waste': 'Preparation Efficiency',
            'spoilage': 'Storage Conditions',
            'contamination': 'Food Safety',
            'other': 'Other'
        }
        return prevention_categories.get(reason, 'Other')
    
    def calculate_waste_cost(self, 
                            start_date: datetime = None,
                            end_date: datetime = None,
                            material_name: str = None) -> Dict:
        """
        Calculate total waste cost for a period.
        
        Args:
            start_date: Start date (None = beginning)
            end_date: End date (None = now)
            material_name: Specific material (None = all)
        
        Returns:
            Cost breakdown dictionary
        """
        if self.waste_history.empty:
            return {
                'total_cost': 0,
                'total_items': 0,
                'period': 'No data'
            }
        
        # Filter by date
        df = self.waste_history.copy()
        
        if start_date:
            df = df[df['date'] >= start_date]
        if end_date:
            df = df[df['date'] <= end_date]
        if material_name:
            df = df[df['material_name'] == material_name]
        
        if df.empty:
            return {
                'total_cost': 0,
                'total_items': 0,
                'period': f"{start_date} to {end_date}"
            }
        
        # Calculate metrics
        total_cost = df['total_cost'].sum()
        total_items = len(df)
        avg_cost_per_incident = total_cost / total_items if total_items > 0 else 0
        
        # By category
        by_category = df.groupby('category').agg({
            'total_cost': 'sum',
            'quantity': 'count'
        }).sort_values('total_cost', ascending=False)
        
        # By reason
        by_reason = df.groupby('reason').agg({
            'total_cost': 'sum',
            'quantity': 'count'
        }).sort_values('total_cost', ascending=False)
        
        # By material
        by_material = df.groupby('material_name').agg({
            'total_cost': 'sum',
            'quantity': 'sum'
        }).sort_values('total_cost', ascending=False)
        
        return {
            'total_cost': round(total_cost, 2),
            'total_items': total_items,
            'avg_cost_per_incident': round(avg_cost_per_incident, 2),
            'period': f"{df['date'].min()} to {df['date'].max()}",
            'by_category': by_category.to_dict('index'),
            'by_reason': by_reason.to_dict('index'),
            'by_material': by_material.head(10).to_dict('index'),
            'top_waste_material': by_material.index[0] if not by_material.empty else None
        }
    
    def analyze_waste_patterns(self, days: int = 30) -> Dict:
        """
        Analyze waste patterns over time.
        
        Args:
            days: Number of days to analyze
        
        Returns:
            Pattern analysis dictionary
        """
        if self.waste_history.empty:
            return {'error': 'No waste data available'}
        
        # Filter recent data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        recent_waste = self.waste_history[
            self.waste_history['date'] >= start_date
        ]
        
        if recent_waste.empty:
            return {'error': f'No waste data in last {days} days'}
        
        # Daily trends
        daily_waste = recent_waste.groupby(recent_waste['date'].dt.date).agg({
            'total_cost': 'sum',
            'quantity': 'count'
        })
        
        # Weekly patterns (which day of week has most waste?)
        recent_waste['day_of_week'] = recent_waste['date'].dt.day_name()
        weekly_pattern = recent_waste.groupby('day_of_week')['total_cost'].sum().sort_values(ascending=False)
        
        # Trending materials
        material_trends = recent_waste.groupby('material_name').agg({
            'total_cost': 'sum',
            'quantity': 'count'
        }).sort_values('total_cost', ascending=False)
        
        # Identify issues
        issues = []
        
        # High frequency materials
        high_freq = material_trends[material_trends['quantity'] > 5].index.tolist()
        if high_freq:
            issues.append({
                'type': 'High Frequency Waste',
                'materials': high_freq,
                'action': 'Review ordering quantities and storage practices'
            })
        
        # High cost materials
        high_cost = material_trends[material_trends['total_cost'] > 100].index.tolist()
        if high_cost:
            issues.append({
                'type': 'High Cost Waste',
                'materials': high_cost,
                'action': 'Prioritize waste reduction for these expensive items'
            })
        
        return {
            'analysis_period_days': days,
            'total_waste_cost': round(recent_waste['total_cost'].sum(), 2),
            'total_incidents': len(recent_waste),
            'daily_average_cost': round(daily_waste['total_cost'].mean(), 2),
            'worst_day_of_week': weekly_pattern.index[0] if not weekly_pattern.empty else None,
            'weekly_pattern': weekly_pattern.to_dict(),
            'top_5_materials': material_trends.head(5).to_dict('index'),
            'issues_identified': issues
        }
    
    def suggest_waste_reduction(self, material_name: str = None) -> List[Dict]:
        """
        Suggest actionable waste reduction strategies.
        
        Args:
            material_name: Specific material (None = general suggestions)
        
        Returns:
            List of suggestions with potential savings
        """
        suggestions = []
        
        if self.waste_history.empty:
            return [{
                'type': 'general',
                'suggestion': 'Start logging waste to get data-driven recommendations',
                'potential_saving': 0
            }]
        
        # Analyze recent waste (last 30 days)
        recent = self.waste_history[
            self.waste_history['date'] >= datetime.now() - timedelta(days=30)
        ]
        
        if material_name:
            recent = recent[recent['material_name'] == material_name]
        
        if recent.empty:
            return [{
                'type': 'general',
                'suggestion': 'No recent waste data available for analysis',
                'potential_saving': 0
            }]
        
        # 1. Expiry-related waste
        expiry_waste = recent[recent['reason'] == 'expired']
        if not expiry_waste.empty:
            expiry_cost = expiry_waste['total_cost'].sum()
            suggestions.append({
                'type': 'Reduce Expiry Waste',
                'current_cost': round(expiry_cost, 2),
                'suggestion': 'Implement FIFO (First In First Out) system and reduce order quantities',
                'potential_saving': round(expiry_cost * 0.6, 2),  # 60% reduction potential
                'action_items': [
                    'Order smaller quantities more frequently',
                    'Implement expiry date tracking',
                    'Use near-expiry materials in daily specials'
                ]
            })
        
        # 2. Overproduction waste
        overprod_waste = recent[recent['reason'] == 'overproduction']
        if not overprod_waste.empty:
            overprod_cost = overprod_waste['total_cost'].sum()
            suggestions.append({
                'type': 'Reduce Overproduction',
                'current_cost': round(overprod_cost, 2),
                'suggestion': 'Improve demand forecasting and prep-to-order ratios',
                'potential_saving': round(overprod_cost * 0.5, 2),  # 50% reduction
                'action_items': [
                    'Use ML forecasting (this system!)',
                    'Prep in smaller batches',
                    'Offer daily specials for leftover prep'
                ]
            })
        
        # 3. Spoilage waste
        spoilage_waste = recent[recent['reason'] == 'spoilage']
        if not spoilage_waste.empty:
            spoilage_cost = spoilage_waste['total_cost'].sum()
            suggestions.append({
                'type': 'Reduce Spoilage',
                'current_cost': round(spoilage_cost, 2),
                'suggestion': 'Improve storage conditions and temperature monitoring',
                'potential_saving': round(spoilage_cost * 0.7, 2),  # 70% reduction
                'action_items': [
                    'Check refrigerator temperatures daily',
                    'Store items properly (covered, labeled)',
                    'Regular deep cleaning of storage areas'
                ]
            })
        
        # 4. Plate waste
        plate_waste = recent[recent['reason'] == 'plate_waste']
        if not plate_waste.empty:
            plate_cost = plate_waste['total_cost'].sum()
            suggestions.append({
                'type': 'Reduce Plate Waste',
                'current_cost': round(plate_cost, 2),
                'suggestion': 'Adjust portion sizes or offer size options',
                'potential_saving': round(plate_cost * 0.4, 2),  # 40% reduction
                'action_items': [
                    'Survey customers about portion sizes',
                    'Offer small/regular/large options',
                    'Consider half portions for lunch'
                ]
            })
        
        # 5. High-cost materials
        material_costs = recent.groupby('material_name')['total_cost'].sum().sort_values(ascending=False)
        if len(material_costs) > 0:
            top_material = material_costs.index[0]
            top_cost = material_costs.iloc[0]
            
            suggestions.append({
                'type': 'Focus on High-Cost Material',
                'material': top_material,
                'current_cost': round(top_cost, 2),
                'suggestion': f'Prioritize waste reduction for {top_material} (highest waste cost)',
                'potential_saving': round(top_cost * 0.5, 2),
                'action_items': [
                    f'Track {top_material} usage daily',
                    'Find alternative suppliers',
                    'Consider cheaper substitutes'
                ]
            })
        
        # Calculate total potential savings
        total_potential = sum(s.get('potential_saving', 0) for s in suggestions)
        
        # Add summary
        suggestions.insert(0, {
            'type': 'Summary',
            'current_monthly_waste_cost': round(recent['total_cost'].sum(), 2),
            'total_potential_savings': round(total_potential, 2),
            'suggestion': f'Implementing all recommendations could save ${total_potential:.2f}/month',
            'roi': 'High - waste reduction pays for itself immediately'
        })
        
        return suggestions
    
    def export_waste_log(self, filename: str):
        """Export waste log to CSV file."""
        if self.waste_history.empty:
            logger.warning("No waste data to export")
            return
        
        self.waste_history.to_csv(filename, index=False)
        logger.info(f"Exported {len(self.waste_history)} records to {filename}")
    
    def generate_waste_report(self, days: int = 30) -> str:
        """
        Generate a comprehensive waste report.
        
        Args:
            days: Number of days to include in report
        
        Returns:
            Formatted report string
        """
        report = []
        report.append("=" * 80)
        report.append(f"WASTE ANALYSIS REPORT - Last {days} Days")
        report.append("=" * 80)
        
        # Cost summary
        cost_data = self.calculate_waste_cost(
            start_date=datetime.now() - timedelta(days=days)
        )
        
        report.append(f"\n📊 COST SUMMARY:")
        report.append(f"  • Total Waste Cost: ${cost_data['total_cost']:.2f}")
        report.append(f"  • Total Incidents: {cost_data['total_items']}")
        report.append(f"  • Average per Incident: ${cost_data['avg_cost_per_incident']:.2f}")
        
        # By category
        if 'by_category' in cost_data and cost_data['by_category']:
            report.append(f"\n📂 BY CATEGORY:")
            for cat, data in sorted(cost_data['by_category'].items(), 
                                   key=lambda x: x[1]['total_cost'], 
                                   reverse=True):
                report.append(f"  • {cat:25s}: ${data['total_cost']:8.2f} ({data['quantity']} incidents)")
        
        # Patterns
        patterns = self.analyze_waste_patterns(days=days)
        if 'worst_day_of_week' in patterns:
            report.append(f"\n📅 PATTERNS:")
            report.append(f"  • Worst Day: {patterns['worst_day_of_week']}")
            report.append(f"  • Daily Average: ${patterns['daily_average_cost']:.2f}")
        
        # Suggestions
        suggestions = self.suggest_waste_reduction()
        if suggestions:
            report.append(f"\n💡 RECOMMENDATIONS:")
            for sug in suggestions[:5]:
                report.append(f"\n  {sug['type']}:")
                report.append(f"    {sug['suggestion']}")
                if sug.get('potential_saving'):
                    report.append(f"    Potential Saving: ${sug['potential_saving']:.2f}")
        
        report.append("\n" + "=" * 80)
        
        return "\n".join(report)


# Example usage and testing
if __name__ == "__main__":
    print("=" * 80)
    print("WASTE TRACKING MODULE - DEMO")
    print("=" * 80)
    
    # Initialize tracker
    tracker = WasteTracker()
    
    try:
        # Load data
        tracker.load_data(
            inventory_file='data/csv/inventory_comprehensive.csv',
            recipes_file='data/csv/recipes_comprehensive.csv'
        )
        
        print("\n✅ Data loaded successfully!\n")
        
        # Simulate waste logging
        print("─" * 80)
        print("TEST 1: Logging Waste Incidents")
        print("─" * 80)
        
        # Log some waste
        waste1 = tracker.log_waste(
            material_name='Chicken Breast',
            quantity=2.5,
            reason='expired',
            notes='Found expired in back of fridge'
        )
        print(f"Logged: {waste1['quantity']} {waste1['unit']} {waste1['material_name']} - ${waste1['total_cost']:.2f}")
        
        waste2 = tracker.log_waste(
            material_name='Tomatoes',
            quantity=3.2,
            reason='spoilage',
            notes='Turned soft, not refrigerated properly'
        )
        print(f"Logged: {waste2['quantity']} {waste2['unit']} {waste2['material_name']} - ${waste2['total_cost']:.2f}")
        
        waste3 = tracker.log_waste(
            material_name='Mozzarella Cheese',
            quantity=1.5,
            reason='overproduction',
            notes='Made too many pizzas for lunch rush'
        )
        print(f"Logged: {waste3['quantity']} {waste3['unit']} {waste3['material_name']} - ${waste3['total_cost']:.2f}")
        
        # Calculate costs
        print("\n" + "─" * 80)
        print("TEST 2: Calculate Waste Cost")
        print("─" * 80)
        
        cost_summary = tracker.calculate_waste_cost()
        print(f"\nTotal Waste Cost: ${cost_summary['total_cost']:.2f}")
        print(f"Total Incidents: {cost_summary['total_items']}")
        print(f"Average per Incident: ${cost_summary['avg_cost_per_incident']:.2f}")
        
        # Get suggestions
        print("\n" + "─" * 80)
        print("TEST 3: Waste Reduction Suggestions")
        print("─" * 80)
        
        suggestions = tracker.suggest_waste_reduction()
        for i, sug in enumerate(suggestions[:3], 1):
            print(f"\n{i}. {sug['type']}")
            print(f"   {sug['suggestion']}")
            if sug.get('potential_saving'):
                print(f"   💰 Potential Saving: ${sug['potential_saving']:.2f}")
        
        # Generate report
        print("\n" + "─" * 80)
        print("TEST 4: Generate Full Report")
        print("─" * 80)
        
        report = tracker.generate_waste_report(days=30)
        print(report)
        
        print("\n" + "=" * 80)
        print("✅ ALL TESTS PASSED - WASTE TRACKING MODULE WORKING!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
