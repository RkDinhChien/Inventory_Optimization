# ⚠️ macOS Setup Required

## Vấn đề hiện tại:
Bạn cần cài đặt **Xcode Command Line Tools** để Python có thể chạy các thư viện cần thiết.

## 🔧 Giải pháp - 3 Bước đơn giản:

### Bước 1️⃣: Cài đặt Xcode Command Line Tools

Mở Terminal và chạy lệnh:
```bash
xcode-select --install
```

Một cửa sổ popup sẽ xuất hiện:
- Click **"Install"**
- Đợi khoảng 5-10 phút để cài đặt
- Click **"Done"** khi hoàn tất

### Bước 2️⃣: Kiểm tra Python hoạt động

Sau khi cài xong Xcode Command Line Tools, test Python:
```bash
python3 --version
python3 -c "print('Python works!')"
```

Nếu thấy output không có lỗi → OK! 🎉

### Bước 3️⃣: Chạy Setup Script

```bash
cd "/Users/rykan/ĐỒ ÁN/Inventory_Optimization"
./setup.sh
```

Script này sẽ tự động:
- ✅ Cài đặt tất cả dependencies
- ✅ Cài đặt ML libraries (SARIMA, XGBoost, Prophet)
- ✅ Chạy test kiểm tra hệ thống
- ✅ Hiển thị hướng dẫn sử dụng

---

## 🚀 Sau khi setup xong:

### Demo không cần ML (nhanh):
```bash
python3 demo_quick.py
```

### Demo so sánh ML algorithms:
```bash
python3 demo_ml.py
```

### Test hệ thống:
```bash
python3 test_simple.py
```

### Chạy hệ thống chính:
```bash
python3 main.py
```

---

## 📊 Thuật toán đã tích hợp:

1. **Statistical Method** ✅ (sẵn sàng - không cần ML libs)
   - Nhanh, đơn giản, đủ cho hầu hết trường hợp
   
2. **SARIMA** 🤖 (sau khi setup)
   - Time series forecasting với seasonal patterns
   
3. **XGBoost** 🤖 (sau khi setup)
   - Độ chính xác cao nhất, phù hợp patterns phức tạp
   
4. **Random Forest** 🤖 (sau khi setup)
   - Balanced, robust predictions
   
5. **Prophet** 🤖 (sau khi setup)
   - Facebook's tool, tốt cho holidays và trends

---

## ❓ Nếu gặp vấn đề:

### "xcode-select: command not found"
→ Bạn đang dùng macOS. Cần cài Xcode Command Line Tools (xem Bước 1)

### "pip3: command not found"
```bash
# Install pip
python3 -m ensurepip --upgrade
```

### "Permission denied"
```bash
# Add sudo or use --user flag
pip3 install --user pandas numpy
```

### Vẫn không được?
Liên hệ hoặc xem log chi tiết:
```bash
python3 demo_quick.py 2>&1 | tee error.log
```

---

## 📖 Tài liệu:

- `README.md` - Tổng quan dự án
- `ML_GUIDE.md` - Chi tiết về ML algorithms
- `README_detailed.md` - Hướng dẫn chi tiết

## 💡 Lưu ý:

- Statistical method hoạt động **ngay lập tức** không cần setup
- ML methods cần cài libraries nhưng cho **accuracy cao hơn**
- Tất cả code đã **production-ready** với error handling tốt

---

**Tác giả:** Inventory Optimization Team  
**Ngày:** November 28, 2025
