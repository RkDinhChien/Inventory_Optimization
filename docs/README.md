# 📚 INVENTORY OPTIMIZATION SYSTEM - DOCUMENTATION

## 📖 Quick Links

- **[Main README](../README.md)**: Project overview and quick start
- **[Detailed Guide](./DETAILED_GUIDE.md)**: In-depth technical documentation
- **[ML Guide](./ML_GUIDE.md)**: Machine Learning algorithms explanation
- **[Slide Info](./SLIDE_INFO.md)**: Presentation materials (Vietnamese)
- **[Setup Guide](./SETUP_GUIDE.md)**: Installation instructions

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run quick demo (no ML)
python demo_quick.py

# 3. Run ML comparison
python demo_ml.py

# 4. Run full system
python main.py
```

---

## 📂 Project Structure

```
Inventory_Optimization/
├── src/                    # Source code
│   ├── inventory_optimizer.py  # Core optimizer (525 lines)
│   ├── ml_forecaster.py        # ML algorithms (385 lines)
│   └── visualizer.py           # Charts & plots (302 lines)
├── data/csv/              # Data files
├── demo_quick.py          # Quick demo (no ML)
├── demo_ml.py             # ML vs Statistical comparison
├── main.py                # Main entry point
└── tests/                 # Unit tests

Total: ~2,200 lines of clean, modular code
```

---

## 🤖 ML Algorithms Supported

1. **SARIMA** - Seasonal ARIMA for time series
2. **XGBoost** - Gradient boosting (highest accuracy)
3. **Random Forest** - Ensemble learning
4. **Prophet** - Facebook's forecasting library
5. **Statistical** - Fast baseline method

---

## 📊 Features

✅ Demand forecasting (7-365 days)
✅ Material requirements calculation
✅ Restocking optimization
✅ Near-expiry alerts
✅ Dish recommendations
✅ Interactive visualizations

---

## 🧪 Testing

```bash
# Run all tests
python test_simple.py
python test_ml.py

# Or use pytest
pytest tests/
```

---

## 📝 Documentation Files

This `docs/` folder contains:
- Technical guides
- Setup instructions
- Slide materials
- Algorithm explanations

All consolidated from root-level markdown files for better organization.
