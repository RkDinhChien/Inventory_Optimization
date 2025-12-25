# 🤝 CONTRIBUTING GUIDELINES

## 📋 Code Standards

### ✅ **Good Practices (Currently Following)**

1. **Modular Code**: Max 600 lines per file
   - ✓ `inventory_optimizer.py`: 525 lines
   - ✓ `ml_forecaster.py`: 385 lines
   - ✓ `visualizer.py`: 302 lines

2. **No Hardcoded Secrets**: 
   - ✓ No API keys in code
   - ✓ Use environment variables or config files

3. **Clean Dependencies**:
   - ✓ All dependencies in `requirements.txt`
   - ✓ No external API dependencies

4. **Testing**:
   - ✓ Unit tests in `tests/`
   - ✓ Integration tests in `test_*.py`

5. **Documentation**:
   - ✓ Clear docstrings
   - ✓ Type hints where appropriate
   - ✓ README with examples

---

## 🚫 **Anti-Patterns to Avoid**

❌ **Database in JSON**: Use CSV/SQLite/proper DB  
❌ **Exposed API Keys**: Never hardcode secrets  
❌ **10K+ line files**: Split into modules  
❌ **Too many MD files**: Keep docs organized  
❌ **Unused test files**: Remove or consolidate  
❌ **Tight coupling**: Changes shouldn't break unrelated features  

---

## 📝 **Code Style**

```python
# Use type hints
def forecast_demand(self, days_ahead: int) -> pd.DataFrame:
    """
    Forecast demand for specified days.
    
    Args:
        days_ahead: Number of days to forecast
        
    Returns:
        DataFrame with forecasts
    """
    pass

# Keep functions small (<50 lines)
# Use descriptive names
# Add comments for complex logic
```

---

## 🧪 **Testing Requirements**

Before submitting:
1. Run all tests: `python test_simple.py && python test_ml.py`
2. Check no hardcoded secrets: `grep -r "API.*KEY" src/`
3. Verify file sizes: `wc -l src/*.py`
4. Update docs if needed

---

## 📊 **Project Metrics**

**Current Status:**
- Total lines: ~2,230
- Largest file: 525 lines ✓
- Test coverage: Basic ✓
- Documentation: Complete ✓
- Security: No exposed secrets ✓

---

## 🔄 **Pull Request Checklist**

- [ ] Code follows style guide
- [ ] Tests pass
- [ ] No secrets hardcoded
- [ ] Documentation updated
- [ ] File sizes reasonable (<600 lines)
- [ ] No breaking changes without notice
