# CHANGELOG - Lịch sử phát triển

## Version 1.0.0 (20/11/2025)

### ✨ Tính năng chính
- Phát hiện xe máy (loại trừ xe đạp và người đi bộ)
- Phát hiện người không đội mũ bảo hiểm
- Kiểm tra người có ngồi trên xe hay không
- Lưu ảnh vi phạm tự động (cooldown 3 giây)
- Giao diện web hiện đại với Tailwind CSS
- Chọn camera linh hoạt qua dropdown
- Tool test với video file

### 🎨 Giao diện
- Header với logo trường THCS Gò Đen
- Video feed real-time với khung màu gradient
- Danh sách vi phạm hiển thị theo dạng gallery
- Footer với thông tin liên hệ
- Responsive design (tương thích mobile)

### ⚡ Tối ưu hóa
- Giảm độ phân giải xuống 640x480
- Chỉ xử lý mỗi 3 frame (giảm tải CPU)
- Sử dụng YOLOv8n (nano) - model nhẹ nhất
- imgsz=320 (thay vì 640) cho inference nhanh hơn
- Buffer size = 1 để giảm lag

### 🐛 Sửa lỗi
- Fix lỗi PyTorch DLL (downgrade về 2.0.1)
- Fix lỗi NumPy compatibility (downgrade về 1.26.4)
- Fix lỗi camera DirectShow trên Windows
- Fix lỗi server tự động thoát khi background
- Fix lỗi khung hình bị nhiễu (thêm warm-up frames)

### 📚 Tài liệu
- HUONG_DAN_CAI_DAT.md - Hướng dẫn chi tiết
- README.txt - Hướng dẫn nhanh
- setup.bat - Script cài đặt tự động
- start.bat - Script khởi động

### 🔧 Cấu hình
- Confidence threshold: 0.3 (có thể điều chỉnh)
- IOU threshold: 0.4
- Frame skip: 3
- Cooldown: 3 giây
- Resolution: 640x480

---

## Kế hoạch phát triển

### Version 1.1 (Tương lai)
- [ ] Thống kê vi phạm theo ngày/tuần/tháng
- [ ] Xuất báo cáo PDF/Excel
- [ ] Gửi thông báo qua email/SMS
- [ ] Nhận dạng biển số xe
- [ ] Database lưu trữ vi phạm

### Version 1.2 (Tương lai)
- [ ] Multi-camera support (nhiều camera cùng lúc)
- [ ] Cloud storage cho ảnh vi phạm
- [ ] Mobile app Android/iOS
- [ ] API RESTful cho tích hợp
- [ ] Dashboard quản trị nâng cao

---

**Ghi chú:** Changelog này được cập nhật theo từng phiên bản phát hành.
