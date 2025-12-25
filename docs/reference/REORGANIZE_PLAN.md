# 📁 FILE REORGANIZATION PLAN

## 🎯 Mục tiêu
- Tổ chức lại cấu trúc file rõ ràng, chuyên nghiệp
- Gom các file MD theo chủ đề vào folders riêng
- Dễ dàng tìm kiếm và maintain

---

## 📂 Cấu trúc MỚI

```
Inventory_Optimization/
│
├── 📄 README.md                    (Main documentation - giữ root)
├── 📄 requirements.txt
├── 📄 setup.sh
│
├── 📁 docs/
│   ├── 📁 guides/                  (User guides - Hướng dẫn người dùng)
│   │   ├── QUICK_START.md
│   │   ├── GIẢI_THÍCH_KẾT_QUẢ.md
│   │   ├── VISUAL_GUIDE.md
│   │   └── INSTALL_FIRST.txt
│   │
│   ├── 📁 technical/               (Technical docs - Tài liệu kỹ thuật)
│   │   ├── MATHEMATICAL_FORMULATION.md
│   │   ├── SYSTEM_ANALYSIS.md
│   │   ├── INTEGRATION_COMPLETE.md
│   │   └── IMPLEMENTATION_COMPLETE.md
│   │
│   ├── 📁 reports/                 (Reports & Status - Báo cáo)
│   │   ├── SYSTEM_HEALTH_CHECK.md
│   │   ├── TEST_REPORT.md
│   │   ├── FIXES_COMPLETED.md
│   │   ├── CLEANUP_REPORT.md
│   │   └── DATASET_EVALUATION.md
│   │
│   └── 📁 reference/               (Reference materials - Tham khảo)
│       ├── CHANGELOG.md
│       ├── CONTRIBUTING.md
│       ├── SLIDE_INFO.md
│       └── QUICKREF.txt
│
├── 📁 src/                         (Source code - Core modules)
│   ├── inventory_optimizer.py
│   ├── ml_forecaster.py
│   ├── cost_analyzer.py
│   ├── waste_tracker.py
│   ├── weather_integration.py
│   ├── market_factors.py
│   └── visualizer.py
│
├── 📁 data/
│   └── csv/
│       ├── recipes_comprehensive.csv
│       ├── inventory_comprehensive.csv
│       └── orders_real.csv
│
├── 📁 scripts/                     (Utility scripts - Di chuyển demos & tools)
│   ├── demo/
│   │   ├── demo_quick.py
│   │   ├── demo_comparison.py
│   │   ├── demo_comprehensive_forecast.py
│   │   └── ...
│   │
│   └── utils/
│       ├── fix_data_timeline.py
│       └── ...
│
├── 📁 tests/                       (Test files)
│   ├── test_inventory_optimizer.py
│   ├── test_ml_forecaster.py
│   └── ...
│
└── 📄 app.py                       (Streamlit app - giữ root)
```

---

## 🔄 Di chuyển FILES

### Bước 1: User Guides
```bash
mv QUICK_START.md docs/guides/
mv GIẢI_THÍCH_KẾT_QUẢ.md docs/guides/
mv VISUAL_GUIDE.md docs/guides/
mv INSTALL_FIRST.txt docs/guides/
```

### Bước 2: Technical Docs
```bash
mv MATHEMATICAL_FORMULATION.md docs/technical/
mv SYSTEM_ANALYSIS.md docs/technical/
mv INTEGRATION_COMPLETE.md docs/technical/
mv IMPLEMENTATION_COMPLETE.md docs/technical/
mv INTEGRATION_SUCCESS.md docs/technical/
```

### Bước 3: Reports
```bash
mv SYSTEM_HEALTH_CHECK.md docs/reports/
mv TEST_REPORT.md docs/reports/
mv FIXES_COMPLETED.md docs/reports/
mv CLEANUP_REPORT.md docs/reports/
mv DATASET_EVALUATION.md docs/reports/
```

### Bước 4: Reference
```bash
mv CHANGELOG.md docs/reference/
mv CONTRIBUTING.md docs/reference/
mv SLIDE_INFO.md docs/reference/
mv QUICKREF.txt docs/reference/
```

### Bước 5: Scripts/Demos
```bash
mkdir -p scripts/demo scripts/utils
mv demo*.py scripts/demo/
mv fix_data_timeline.py scripts/utils/
mv CONG_THUC_MO_RONG.py scripts/utils/
mv HUONG_DAN_APP.py scripts/utils/
mv LUONG_LOGIC.py scripts/utils/
```

---

## ✅ Files GIỮ LẠI root level

- `README.md` - Main entry point
- `app.py` - Streamlit application
- `main.py` - Main entry script
- `requirements.txt` - Dependencies
- `setup.sh` - Setup script

---

## 📝 UPDATE README với links mới

Sau khi di chuyển, update README.md với links tới các docs mới:

```markdown
## 📚 Documentation

### 🎓 User Guides
- [Quick Start](docs/guides/QUICK_START.md)
- [Giải Thích Kết Quả](docs/guides/GIẢI_THÍCH_KẾT_QUẢ.md)
- [Visual Guide](docs/guides/VISUAL_GUIDE.md)

### 🔧 Technical Documentation
- [Mathematical Formulation](docs/technical/MATHEMATICAL_FORMULATION.md)
- [System Analysis](docs/technical/SYSTEM_ANALYSIS.md)
- [Integration Guide](docs/technical/INTEGRATION_COMPLETE.md)

### �� Reports & Status
- [System Health Check](docs/reports/SYSTEM_HEALTH_CHECK.md)
- [Test Report](docs/reports/TEST_REPORT.md)
- [Fixes Completed](docs/reports/FIXES_COMPLETED.md)
```

---

## ⚠️ Lưu ý

1. **Git tracking**: Sau khi move, commit changes
2. **Update imports**: Nếu có script import relative paths
3. **CI/CD**: Update paths trong workflows (nếu có)
4. **Links**: Update all internal links trong docs

---

**Status**: READY TO EXECUTE
**Estimated Time**: 10-15 minutes
**Risk**: LOW (có thể revert bằng git)
