"""
COST ANALYSIS MODULE
Comprehensive cost tracking, profitability analysis, and pricing recommendations
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CostAnalyzer:
    """Analyze costs, profitability, and pricing for dishes."""
    
    def __init__(self):
        self.recipes_data = None
        self.inventory_data = None
        self.orders_data = None
        self.cost_cache = {}
        
    def load_data(self, recipes_file: str, inventory_file: str, orders_file: str = None):
        """Load necessary data files."""
        try:
            self.recipes_data = pd.read_csv(recipes_file)
            self.inventory_data = pd.read_csv(inventory_file)
            
            if orders_file:
                self.orders_data = pd.read_csv(orders_file)
                if 'date' in self.orders_data.columns:
                    self.orders_data['date'] = pd.to_datetime(self.orders_data['date'])
            
            logger.info(f"Loaded {len(self.recipes_data)} recipe records")
            logger.info(f"Loaded {len(self.inventory_data)} inventory items")
            
            # Create cost lookup for faster access
            self.cost_lookup = dict(zip(
                self.inventory_data['material_name'],
                self.inventory_data['cost_per_unit']
            ))
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def calculate_cogs(self, dish_name: str, servings: int = 1) -> Dict:
        """
        Calculate Cost of Goods Sold (COGS) for a dish.
        
        Returns:
            Dictionary with cost breakdown
        """
        if self.recipes_data is None or self.inventory_data is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        # Check cache
        cache_key = f"{dish_name}_{servings}"
        if cache_key in self.cost_cache:
            return self.cost_cache[cache_key]
        
        # Get recipe
        recipe = self.recipes_data[self.recipes_data['dish_name'] == dish_name]
        
        if recipe.empty:
            logger.warning(f"No recipe found for {dish_name}")
            return {
                'dish_name': dish_name,
                'total_cogs': 0,
                'servings': servings,
                'cogs_per_serving': 0,
                'materials': [],
                'error': 'Recipe not found'
            }
        
        # Calculate costs
        materials = []
        total_cost = 0
        
        for _, row in recipe.iterrows():
            material_name = row['material_name']
            quantity_needed = row['quantity_needed'] * servings
            
            # Get unit cost
            unit_cost = self.cost_lookup.get(material_name, 0)
            
            if unit_cost == 0:
                logger.warning(f"No cost data for {material_name}")
            
            material_cost = quantity_needed * unit_cost
            total_cost += material_cost
            
            materials.append({
                'material_name': material_name,
                'quantity_needed': quantity_needed,
                'unit': row.get('unit', 'kg'),
                'cost_per_unit': unit_cost,
                'cost': round(material_cost, 2),
                'percentage': 0  # Will be calculated below
            })
        
        # Calculate percentages
        if total_cost > 0:
            for mat in materials:
                mat['percentage'] = round((mat['cost'] / total_cost) * 100, 2)
        
        result = {
            'dish_name': dish_name,
            'total_cogs': round(total_cost, 2),
            'servings': servings,
            'cogs_per_serving': round(total_cost / servings, 2) if servings > 0 else 0,
            'materials': materials,
            'material_count': len(materials)
        }
        
        # Cache result
        self.cost_cache[cache_key] = result
        
        return result
    
    def calculate_profit_margin(self, dish_name: str, selling_price: float = None) -> Dict:
        """
        Calculate profit margin for a dish.
        
        Args:
            dish_name: Name of the dish
            selling_price: Selling price (if None, tries to get from orders_data)
        
        Returns:
            Dictionary with profit analysis
        """
        # Get COGS
        cogs_data = self.calculate_cogs(dish_name, servings=1)
        cogs = cogs_data['cogs_per_serving']
        
        # Get selling price if not provided
        if selling_price is None and self.orders_data is not None:
            dish_orders = self.orders_data[self.orders_data['dish_name'] == dish_name]
            if not dish_orders.empty and 'checkout_price' in dish_orders.columns:
                selling_price = dish_orders['checkout_price'].mean()
            else:
                selling_price = 0
        
        if selling_price == 0:
            return {
                'dish_name': dish_name,
                'cogs': cogs,
                'selling_price': 0,
                'gross_profit': 0,
                'profit_margin_percent': 0,
                'markup_percent': 0,
                'error': 'No selling price available'
            }
        
        # Calculate metrics
        gross_profit = selling_price - cogs
        profit_margin = (gross_profit / selling_price) * 100 if selling_price > 0 else 0
        markup = (gross_profit / cogs) * 100 if cogs > 0 else 0
        
        return {
            'dish_name': dish_name,
            'cogs': round(cogs, 2),
            'selling_price': round(selling_price, 2),
            'gross_profit': round(gross_profit, 2),
            'profit_margin_percent': round(profit_margin, 2),
            'markup_percent': round(markup, 2),
            'contribution_margin': round(gross_profit, 2)
        }
    
    def recommend_pricing(self, dish_name: str, target_margin: float = 30.0) -> Dict:
        """
        Recommend optimal pricing based on target profit margin.
        
        Args:
            dish_name: Name of the dish
            target_margin: Target profit margin % (default 30%)
        
        Returns:
            Pricing recommendations
        """
        cogs_data = self.calculate_cogs(dish_name, servings=1)
        cogs = cogs_data['cogs_per_serving']
        
        if cogs == 0:
            return {
                'dish_name': dish_name,
                'error': 'Cannot calculate pricing - COGS is zero'
            }
        
        # Calculate recommended price for target margin
        recommended_price = cogs / (1 - target_margin/100)
        profit = recommended_price - cogs
        markup_percent = (profit/cogs)*100 if cogs > 0 else 0
        
        # Calculate recommended prices for different margins
        margins = [20, 25, 30, 35, 40, 45, 50]
        recommendations = []
        
        for margin in margins:
            price = cogs / (1 - margin/100)
            profit_margin = price - cogs
            
            recommendations.append({
                'target_margin': margin,
                'recommended_price': round(price, 2),
                'gross_profit': round(profit_margin, 2),
                'markup_percent': round((profit_margin/cogs)*100, 2)
            })
        
        # Get current price if available
        current_price = None
        current_margin = None
        
        if self.orders_data is not None:
            dish_orders = self.orders_data[self.orders_data['dish_name'] == dish_name]
            if not dish_orders.empty and 'checkout_price' in dish_orders.columns:
                current_price = dish_orders['checkout_price'].mean()
                current_profit = current_price - cogs
                current_margin = (current_profit / current_price) * 100 if current_price > 0 else 0
        
        return {
            'dish_name': dish_name,
            'cogs': round(cogs, 2),
            'recommended_price': round(recommended_price, 2),
            'profit': round(profit, 2),
            'markup_percent': round(markup_percent, 2),
            'current_price': round(current_price, 2) if current_price else None,
            'current_margin': round(current_margin, 2) if current_margin else None,
            'recommendations': recommendations,
            'recommended_price_30pct': round(cogs / 0.7, 2),  # 30% margin
            'recommended_price_35pct': round(cogs / 0.65, 2),  # 35% margin
            'recommended_price_40pct': round(cogs / 0.6, 2)    # 40% margin
        }
    
    def analyze_menu_profitability(self) -> pd.DataFrame:
        """
        Analyze profitability of entire menu.
        
        Returns:
            DataFrame with profitability analysis for all dishes
        """
        if self.recipes_data is None:
            raise ValueError("Data not loaded")
        
        all_dishes = self.recipes_data['dish_name'].unique()
        results = []
        
        for dish in all_dishes:
            try:
                # Get COGS
                cogs_data = self.calculate_cogs(dish)
                cogs = cogs_data['cogs_per_serving']
                
                # Get selling data
                selling_price = 0
                total_revenue = 0
                total_sold = 0
                
                if self.orders_data is not None:
                    dish_orders = self.orders_data[self.orders_data['dish_name'] == dish]
                    if not dish_orders.empty:
                        if 'checkout_price' in dish_orders.columns:
                            selling_price = dish_orders['checkout_price'].mean()
                        if 'quantity_sold' in dish_orders.columns:
                            total_sold = dish_orders['quantity_sold'].sum()
                            if 'checkout_price' in dish_orders.columns:
                                total_revenue = (dish_orders['checkout_price'] * dish_orders['quantity_sold']).sum()
                
                # Calculate metrics
                gross_profit = selling_price - cogs if selling_price > 0 else 0
                profit_margin = (gross_profit / selling_price * 100) if selling_price > 0 else 0
                total_profit = gross_profit * total_sold
                total_cogs = cogs * total_sold
                
                results.append({
                    'dish_name': dish,
                    'cogs': round(cogs, 2),
                    'selling_price': round(selling_price, 2),
                    'gross_profit': round(gross_profit, 2),
                    'profit_margin_pct': round(profit_margin, 2),
                    'total_sold': int(total_sold),
                    'total_revenue': round(total_revenue, 2),
                    'total_cogs': round(total_cogs, 2),
                    'total_profit': round(total_profit, 2),
                    'material_count': cogs_data['material_count']
                })
                
            except Exception as e:
                logger.error(f"Error analyzing {dish}: {e}")
                continue
        
        df = pd.DataFrame(results)
        
        # Sort by profitability
        if not df.empty and 'total_profit' in df.columns:
            df = df.sort_values('total_profit', ascending=False)
        
        return df
    
    def identify_high_cost_materials(self, dish_name: str = None) -> pd.DataFrame:
        """
        Identify materials that contribute most to costs.
        
        Args:
            dish_name: Specific dish (None for all dishes)
        
        Returns:
            DataFrame with material cost analysis
        """
        if dish_name:
            dishes = [dish_name]
        else:
            dishes = self.recipes_data['dish_name'].unique()
        
        material_costs = []
        
        for dish in dishes:
            cogs_data = self.calculate_cogs(dish)
            for mat in cogs_data['materials']:
                material_costs.append({
                    'dish_name': dish,
                    'material_name': mat['material_name'],
                    'quantity_needed': mat['quantity_needed'],
                    'unit': mat['unit'],
                    'cost_per_unit': mat['cost_per_unit'],
                    'total_cost': mat['cost'],
                    'cost_percentage': mat['percentage']
                })
        
        df = pd.DataFrame(material_costs)
        
        if not df.empty:
            # Sort by total cost
            df = df.sort_values('total_cost', ascending=False)
        
        return df
    
    def suggest_cost_reductions(self, dish_name: str) -> List[Dict]:
        """
        Suggest ways to reduce costs for a dish.
        
        Returns:
            List of cost reduction suggestions
        """
        cogs_data = self.calculate_cogs(dish_name)
        materials = cogs_data['materials']
        
        suggestions = []
        
        # Identify expensive materials (>20% of cost)
        for mat in materials:
            if mat['percentage'] > 20:
                suggestions.append({
                    'type': 'expensive_ingredient',
                    'material': mat['material_name'],
                    'current_cost': mat['cost'],
                    'percentage': mat['percentage'],
                    'suggestion': f"Consider cheaper alternative for {mat['material_name']} (currently {mat['percentage']}% of cost)",
                    'potential_saving': round(mat['cost'] * 0.2, 2)  # 20% reduction estimate
                })
        
        # Identify small quantities that could be increased
        for mat in materials:
            if mat['quantity_needed'] < 0.05 and mat['percentage'] > 5:
                suggestions.append({
                    'type': 'small_quantity_expensive',
                    'material': mat['material_name'],
                    'current_quantity': mat['quantity_needed'],
                    'percentage': mat['percentage'],
                    'suggestion': f"Very small quantity ({mat['quantity_needed']} {mat['unit']}) but high cost impact ({mat['percentage']}%) - verify necessity",
                    'potential_saving': round(mat['cost'] * 0.5, 2)
                })
        
        # General suggestion if no specific issues
        if len(suggestions) == 0:
            suggestions.append({
                'type': 'general',
                'suggestion': f"Cost structure looks balanced for {dish_name}. Consider negotiating bulk discounts with suppliers.",
                'potential_saving': round(cogs_data['total_cogs'] * 0.05, 2)  # 5% estimate
            })
        
        return suggestions


# Example usage and testing
if __name__ == "__main__":
    print("=" * 80)
    print("COST ANALYSIS MODULE - DEMO")
    print("=" * 80)
    
    # Initialize analyzer
    analyzer = CostAnalyzer()
    
    try:
        # Load data
        analyzer.load_data(
            recipes_file='data/csv/recipes_comprehensive.csv',
            inventory_file='data/csv/inventory_comprehensive.csv',
            orders_file='data/csv/orders_real.csv'
        )
        
        print("\n✅ Data loaded successfully!\n")
        
        # Test COGS calculation
        print("─" * 80)
        print("TEST 1: Calculate COGS for Biryani_Indian")
        print("─" * 80)
        
        cogs_data = analyzer.calculate_cogs('Biryani_Indian', servings=1)
        print(f"\nDish: {cogs_data['dish_name']}")
        print(f"Total COGS: ${cogs_data['total_cogs']:.2f}")
        print(f"Materials used: {cogs_data['material_count']}")
        
        print("\nMaterial Breakdown:")
        for mat in sorted(cogs_data['materials'], key=lambda x: x['percentage'], reverse=True)[:5]:
            print(f"  • {mat['material_name']:20s}: ${mat['cost']:6.2f} ({mat['percentage']:5.1f}%)")
        
        # Test profit margin
        print("\n" + "─" * 80)
        print("TEST 2: Calculate Profit Margin")
        print("─" * 80)
        
        profit_data = analyzer.calculate_profit_margin('Biryani_Indian')
        print(f"\nDish: {profit_data['dish_name']}")
        print(f"COGS: ${profit_data['cogs']:.2f}")
        print(f"Selling Price: ${profit_data['selling_price']:.2f}")
        print(f"Gross Profit: ${profit_data['gross_profit']:.2f}")
        print(f"Profit Margin: {profit_data['profit_margin_percent']:.2f}%")
        print(f"Markup: {profit_data['markup_percent']:.2f}%")
        
        # Test pricing recommendations
        print("\n" + "─" * 80)
        print("TEST 3: Pricing Recommendations")
        print("─" * 80)
        
        pricing = analyzer.recommend_pricing('Biryani_Indian', target_margin=35)
        print(f"\nDish: {pricing['dish_name']}")
        print(f"COGS: ${pricing['cogs']:.2f}")
        
        if pricing.get('current_price'):
            print(f"Current Price: ${pricing['current_price']:.2f} (Margin: {pricing['current_margin']:.1f}%)")
        
        print("\nRecommended Prices:")
        for rec in pricing['recommendations'][:5]:
            print(f"  • {rec['target_margin']:2.0f}% margin: ${rec['recommended_price']:6.2f} (Profit: ${rec['gross_profit']:5.2f})")
        
        # Test menu profitability
        print("\n" + "─" * 80)
        print("TEST 4: Menu Profitability Analysis")
        print("─" * 80)
        
        menu_analysis = analyzer.analyze_menu_profitability()
        print(f"\n{menu_analysis.head(10).to_string(index=False)}")
        
        # Cost reduction suggestions
        print("\n" + "─" * 80)
        print("TEST 5: Cost Reduction Suggestions")
        print("─" * 80)
        
        suggestions = analyzer.suggest_cost_reductions('Biryani_Indian')
        for i, sug in enumerate(suggestions, 1):
            print(f"\n{i}. {sug.get('suggestion')}")
            if sug.get('potential_saving'):
                print(f"   Potential Saving: ${sug['potential_saving']:.2f}")
        
        print("\n" + "=" * 80)
        print("✅ ALL TESTS PASSED - COST ANALYSIS MODULE WORKING!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
