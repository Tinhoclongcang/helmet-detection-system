# HƯỚNG DẪN CÀI ĐẶT VÀ SỬ DỤNG
## HỆ THỐNG GIÁM SÁT MŨ BẢO HIỂM - TRƯỜNG THCS GÒ ĐEN

---

## 📋 YÊU CẦU HỆ THỐNG

### Phần cứng tối thiểu:
- **CPU:** Intel Pentium Gold G6400 trở lên (hoặc tương đương)
- **RAM:** 8GB
- **Ổ cứng:** 2GB trống
- **Camera:** Webcam USB hoặc camera tích hợp

### Phần mềm:
- **Hệ điều hành:** Windows 10/11 (64-bit)
- **Python:** 3.11.9
- **Visual C++ Redistributable:** 2015-2022

---

## 🚀 CÁCH 1: CÀI ĐẶT NHANH (KHUYẾN NGHỊ)

### Bước 1: Giải nén file
- Giải nén toàn bộ thư mục vào `C:\Users\PC\Documents\duan\`
- Đảm bảo cấu trúc thư mục đúng như sau:

```
duan/
├── app.py
├── best.pt
├── yolov8n.pt
├── start.bat
├── start.ps1
├── test_video.py
├── requirements.txt
├── templates/
│   ├── index.html
│   └── debug.html
└── static/
    └── violations/
```

### Bước 2: Cài đặt Python
1. Tải Python 3.11.9 từ: https://www.python.org/downloads/
2. **QUAN TRỌNG:** Tick chọn "Add Python to PATH"
3. Cài đặt với tùy chọn mặc định

### Bước 3: Cài đặt Visual C++ Redistributable
1. Tải từ: https://aka.ms/vs/17/release/vc_redist.x64.exe
2. Chạy file và cài đặt

### Bước 4: Cài đặt thư viện
Mở PowerShell tại thư mục `duan` và chạy:
```powershell
pip install -r requirements.txt
```

### Bước 5: Khởi động hệ thống
**Cách 1 (Đơn giản nhất):**
- Double-click vào file `start.bat`

**Cách 2 (PowerShell):**
```powershell
.\start.bat
```

### Bước 6: Truy cập hệ thống
- Mở trình duyệt và truy cập: **http://localhost:5000**

---

## 🎯 CÁCH 2: TEST VỚI VIDEO

### Chuẩn bị video test:
1. Đặt video vào thư mục `duan/`
2. Đổi tên thành `test.mp4`
3. Video nên chứa cảnh học sinh đi xe máy

### Chạy test:
```powershell
python test_video.py
```

### Điều khiển:
- **Space:** Tạm dừng/Tiếp tục
- **Q:** Thoát
- Kết quả lưu trong thư mục `test_violations/`

---

## 📖 HƯỚNG DẪN SỬ DỤNG

### Giao diện chính
1. **Camera trực tiếp:** Hiển thị video real-time
2. **Chọn camera:** Dropdown để chuyển nguồn camera
3. **Vi phạm ghi nhận:** Danh sách ảnh vi phạm

### Cách thức hoạt động:
1. ✅ Phát hiện xe máy (màu cam)
2. ✅ Phát hiện người không đội mũ (màu đỏ)
3. ✅ Kiểm tra người có ngồi trên xe
4. ✅ Chụp ảnh vi phạm (mỗi 3 giây/lần)
5. ✅ Lưu ảnh vào `static/violations/`

### Loại trừ:
- ❌ Xe đạp
- ❌ Người đi bộ
- ❌ Người đội mũ đầy đủ

---

## 🔧 XỬ LÝ SỰ CỐ

### Lỗi: "python không được nhận dạng"
**Nguyên nhân:** Python chưa được thêm vào PATH
**Giải pháp:**
1. Gỡ cài đặt Python
2. Cài lại và tick "Add Python to PATH"

### Lỗi: "DLL load failed"
**Nguyên nhân:** Thiếu Visual C++ Redistributable
**Giải pháp:**
- Cài đặt vc_redist.x64.exe từ link trên

### Lỗi: Camera không hiển thị
**Nguyên nhân:** Camera đang bị sử dụng bởi ứng dụng khác
**Giải pháy:**
1. Đóng tất cả ứng dụng camera (Zoom, Teams, Skype...)
2. Khởi động lại hệ thống

### Lỗi: "ERR_CONNECTION_REFUSED"
**Nguyên nhân:** Server chưa khởi động
**Giải pháp:**
- Kiểm tra terminal có dòng "Running on http://127.0.0.1:5000"
- Chạy lại `start.bat`

### Phát hiện chưa nhạy
**Giải pháp:** Giảm confidence trong file `app.py`
```python
# Dòng 101
vehicle_results = vehicle_model(frame, classes=[3], conf=0.25, ...)

# Dòng 119
helmet_results = helmet_model(frame, classes=[1], conf=0.25, ...)
```

---

## 📊 THÔNG SỐ KỸ THUẬT

### Model AI:
- **Phát hiện xe:** YOLOv8n (COCO dataset)
- **Phát hiện mũ:** Hard Hat Detection (custom trained)
- **Độ chính xác:** ~85-90%
- **Tốc độ:** 10-15 FPS trên Pentium G6400

### Camera:
- **Độ phân giải:** 640x480 (VGA)
- **FPS:** 30
- **Backend:** DirectShow (Windows)

### Lưu trữ:
- **Ảnh vi phạm:** JPG format
- **Cooldown:** 3 giây/ảnh
- **Đường dẫn:** `static/violations/`

---

## 🛡️ BẢO MẬT VÀ QUYỀN RIÊNG TƯ

⚠️ **Lưu ý quan trọng:**
- Hệ thống chỉ lưu ảnh khi phát hiện vi phạm
- Tuân thủ quy định về bảo vệ dữ liệu cá nhân
- Chỉ sử dụng cho mục đích giáo dục
- Không chia sẻ ảnh vi phạm công khai

---

## 📞 HỖ TRỢ KỸ THUẬT

**TRƯỜNG THCS GÒ ĐEN**
- Địa chỉ: [Địa chỉ trường]
- Điện thoại: [Số điện thoại]
- Email: [Email liên hệ]

---

## 📝 CHANGELOG

### Version 1.0 (20/11/2025)
- ✅ Phát hiện xe máy + không mũ bảo hiểm
- ✅ Giao diện web hiện đại
- ✅ Chọn camera linh hoạt
- ✅ Tool test video
- ✅ Tối ưu cho CPU yếu

---

**© 2025 - Trường THCS Gò Đen - Hệ thống Giám sát An toàn Giao thông**
