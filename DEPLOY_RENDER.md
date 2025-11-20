# 🚀 Hướng Dẫn Deploy Lên Render.com

## 📋 Tổng Quan

Hệ thống phát hiện vi phạm không đội mũ bảo hiểm với khả năng:
- ✅ Upload video file
- ✅ Phân tích tự động bằng AI (YOLOv8)
- ✅ Hiển thị kết quả và ảnh vi phạm
- ✅ Hoạt động 24/7 trên cloud

---

## 🎯 Bước 1: Chuẩn Bị

### 1.1. Tạo tài khoản GitHub (nếu chưa có)
1. Truy cập https://github.com
2. Đăng ký tài khoản miễn phí
3. Xác thực email

### 1.2. Tạo tài khoản Render.com
1. Truy cập https://render.com
2. Click **"Get Started"**
3. Đăng ký bằng tài khoản GitHub (khuyến nghị)

---

## 📦 Bước 2: Tạo Repository GitHub

### 2.1. Tạo Repository Mới
1. Vào GitHub, click **"New repository"**
2. Đặt tên: `helmet-detection-system`
3. Chọn **Public** (quan trọng cho Render free tier)
4. ✅ Tick "Add a README file"
5. Click **"Create repository"**

### 2.2. Upload Code Lên GitHub

#### Cách 1: Dùng GitHub Desktop (Dễ nhất)
1. Tải GitHub Desktop: https://desktop.github.com
2. Cài đặt và đăng nhập
3. Click **"File"** → **"Add local repository"**
4. Chọn thư mục project của bạn: `HeThongGiamSat_THCS_GoDen_v1.0`
5. Click **"Publish repository"**

#### Cách 2: Dùng Git Command Line
```bash
cd "C:\Users\Tin Hoc Long Cang\Downloads\HeThongGiamSat_THCS_GoDen_v1.0"

git init
git add .
git commit -m "Initial commit - Helmet detection system"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/helmet-detection-system.git
git push -u origin main
```

#### Cách 3: Upload Trực Tiếp (Đơn giản nhất)
1. Vào repository vừa tạo trên GitHub
2. Click **"Add file"** → **"Upload files"**
3. Kéo thả TẤT CẢ các file vào (QUAN TRỌNG: Bao gồm `best.pt` và `yolov8n.pt`)
4. Commit changes

---

## 🌐 Bước 3: Deploy Lên Render.com

### 3.1. Tạo Web Service
1. Đăng nhập vào https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Click **"Build and deploy from a Git repository"**
4. Click **"Connect account"** (nếu chưa kết nối GitHub)

### 3.2. Chọn Repository
1. Tìm repository `helmet-detection-system`
2. Click **"Connect"**

### 3.3. Cấu Hình Web Service

Điền thông tin như sau:

| Trường | Giá trị |
|--------|---------|
| **Name** | `helmet-detection` (hoặc tên bạn muốn) |
| **Region** | `Singapore` (gần Việt Nam nhất) |
| **Branch** | `main` |
| **Root Directory** | (để trống) |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements_render.txt` |
| **Start Command** | `gunicorn app_upload:app` |
| **Instance Type** | **Free** |

### 3.4. Environment Variables (Tùy chọn)
Không cần thiết lập gì thêm cho version cơ bản.

### 3.5. Deploy
1. Click **"Create Web Service"**
2. Chờ 5-10 phút để Render build và deploy
3. Theo dõi logs để xem quá trình deploy

---

## ✅ Bước 4: Kiểm Tra Deployment

### 4.1. Xem Logs
- Trong Render Dashboard, vào tab **"Logs"**
- Kiểm tra xem có lỗi không
- Nếu thấy dòng: `✅ Models đã sẵn sàng!` → Thành công!

### 4.2. Truy Cập Website
1. Lấy URL từ Render Dashboard (dạng: `https://helmet-detection-XXXX.onrender.com`)
2. Copy URL và mở trong trình duyệt
3. Bạn sẽ thấy giao diện upload video

### 4.3. Test Upload Video
1. Upload video test (ví dụ: `test.mp4`)
2. Click **"BẮT ĐẦU PHÂN TÍCH"**
3. Theo dõi progress bar
4. Xem kết quả phát hiện vi phạm

---

## ⚠️ Lưu Ý Quan Trọng

### 🔴 Hạn Chế của Free Tier Render.com
1. **Sleep sau 15 phút không dùng**
   - Web sẽ "ngủ" nếu không có traffic
   - Lần đầu truy cập sau khi ngủ sẽ mất 30-60s để khởi động
   
2. **750 giờ/tháng**
   - Đủ dùng cho demo và testing
   - Reset mỗi đầu tháng
   
3. **Giới hạn tài nguyên**
   - CPU: 0.5 vCPU
   - RAM: 512 MB
   - Xử lý video sẽ CHẬM hơn trên PC
   - Video dài có thể timeout (> 5 phút)

### 💡 Khuyến Nghị
- Dùng video ngắn (< 1 phút) để test
- Giảm resolution video xuống 720p hoặc thấp hơn
- Không upload video > 50MB

---

## 🔧 Troubleshooting

### ❌ Lỗi "Build failed"
**Nguyên nhân:** Thiếu file hoặc lỗi dependencies

**Giải pháp:**
1. Kiểm tra có đầy đủ files không:
   - ✅ `app_upload.py`
   - ✅ `requirements_render.txt`
   - ✅ `Procfile`
   - ✅ `runtime.txt`
   - ✅ `best.pt` và `yolov8n.pt`
   - ✅ Thư mục `templates/` với `upload.html` và `results.html`

2. Xem logs chi tiết trong Render Dashboard

### ❌ Lỗi "Application failed to start"
**Nguyên nhân:** Gunicorn không tìm thấy app

**Giải pháp:**
- Kiểm tra Start Command: `gunicorn app_upload:app` (chính xác)
- Kiểm tra file `app_upload.py` có biến `app = Flask(__name__)` không

### ❌ Lỗi "Models chưa sẵn sàng"
**Nguyên nhân:** Thiếu file model weights (`best.pt`, `yolov8n.pt`)

**Giải pháp:**
1. Upload lại `best.pt` và `yolov8n.pt` lên GitHub
2. Redeploy trên Render

### ❌ Video xử lý quá lâu / Timeout
**Nguyên nhân:** Video quá lớn hoặc dài

**Giải pháp:**
- Dùng video ngắn hơn (< 30 giây)
- Giảm resolution xuống 480p
- Nén video trước khi upload

---

## 🎉 Hoàn Thành!

### 🔗 URL Của Bạn
```
https://helmet-detection-XXXX.onrender.com
```

### 📱 Cách Dùng
1. Mở URL trong trình duyệt (PC hoặc điện thoại đều được)
2. Upload video có xe máy
3. Click "BẮT ĐẦU PHÂN TÍCH"
4. Chờ xử lý (có progress bar)
5. Xem kết quả và ảnh vi phạm

---

## 🚀 Nâng Cấp (Tùy Chọn)

### Nếu Muốn Dùng Lâu Dài
1. **Upgrade Render.com** ($7/tháng)
   - Không bị sleep
   - Nhiều RAM hơn
   - Xử lý nhanh hơn

2. **Dùng Railway.app** (Free $5/tháng)
   - Tương tự Render
   - Deploy đơn giản

3. **Google Cloud Run**
   - Free tier hào phóng
   - Scale tốt hơn

---

## 📞 Hỗ Trợ

Nếu gặp vấn đề:
1. Xem logs trong Render Dashboard
2. Kiểm tra file đã đầy đủ chưa
3. Test local trước: `python app_upload.py`

**Chúc bạn deploy thành công! 🎊**
