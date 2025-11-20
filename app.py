import cv2
import os
import time
import numpy as np
from flask import Flask, render_template, Response, request, jsonify
from ultralytics import YOLO

app = Flask(__name__)

# --- CẤU HÌNH ---
VIOLATION_DIR = "static/violations"
if not os.path.exists(VIOLATION_DIR):
    os.makedirs(VIOLATION_DIR)

# 1. Load Model chuẩn để tìm XE MÁY (Class ID 3 trong COCO là Motorcycle)
print("Dang tai model nhan dien Xe...")
vehicle_model = YOLO("yolov8n.pt") 

# 2. Load Model phát hiện mũ bảo hiểm
# Model classes: 0='Hardhat' (co mu), 1='NO-Hardhat' (khong mu)
print("Dang tai model nhan dien Mu bao hiem...")
helmet_model = YOLO("best.pt")

# Cấu hình Camera (USB Webcam) - Mặc định camera 0
current_camera = 0
cap = None

def init_camera(camera_index):
    global cap
    try:
        if cap is not None:
            cap.release()
            time.sleep(0.5)  # Cho camera thời gian đóng
        cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)  # Windows DirectShow
        
        # Đợi camera khởi động
        time.sleep(1)
        
        if cap.isOpened():
            # Giảm độ phân giải xuống HD để máy Pentium chạy mượt hơn
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            cap.set(cv2.CAP_PROP_FPS, 30)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Giảm buffer để tránh lag
            
            # Đọc thử một vài frame để camera ổn định
            for _ in range(5):
                cap.read()
            
            print(f"Camera {camera_index} khoi tao thanh cong!")
            return True
        else:
            print(f"Khong the mo camera {camera_index}")
            return False
    except Exception as e:
        print(f"Loi khi khoi tao camera {camera_index}: {e}")
        return False

# Khởi tạo camera mặc định
print("Khoi tao camera...")
if not init_camera(current_camera):
    print("CANH BAO: Khong the khoi tao camera mac dinh!")

last_save_time = 0
SAVE_COOLDOWN = 3  # Giây

# Hàm kiểm tra va chạm (Kiểm tra người có ngồi trên xe không)
def is_overlapping(box1, box2):
    # box: [x1, y1, x2, y2]
    x_left = max(box1[0], box2[0])
    y_top = max(box1[1], box2[1])
    x_right = min(box1[2], box2[2])
    y_bottom = min(box1[3], box2[3])

    if x_right < x_left or y_bottom < y_top:
        return False
    return True

def detect_and_process():
    global last_save_time
    frame_count = 0
    
    while True:
        if cap is None or not cap.isOpened():
            # Nếu camera không mở được, trả về frame trắng với thông báo
            blank_frame = 255 * np.ones((480, 640, 3), dtype=np.uint8)
            cv2.putText(blank_frame, "CAMERA KHONG KET NOI", (100, 240), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            ret, buffer = cv2.imencode('.jpg', blank_frame)
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            time.sleep(0.1)
            continue
            
        success, frame = cap.read()
        if not success:
            time.sleep(0.1)
            continue
        
        frame_count += 1
        # Chỉ xử lý mỗi 3 frame một lần để giảm tải cho CPU yếu
        if frame_count % 3 != 0:
            # Vẫn mã hóa frame để video mượt, nhưng không chạy AI
            ret, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            continue

        # --- BƯỚC 1: Tìm Xe Máy (Class 3) ---
        # classes=[3] nghĩa là chỉ tìm Motorcycle. Bỏ qua xe đạp (1) và người đi bộ.
        vehicle_results = vehicle_model(frame, classes=[3], conf=0.3, imgsz=320, verbose=False)
        
        motorcycles = []
        for box in vehicle_results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            motorcycles.append([x1, y1, x2, y2])
            # Vẽ khung xe máy màu Cam
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 165, 255), 2)
            cv2.putText(frame, "Xe May", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 165, 255), 2)

        # --- BƯỚC 2: Nếu có Xe Máy -> Tìm người không nón ---
        violation_confirmed = False
        
        if len(motorcycles) > 0:
            # Tìm người KHÔNG đội mũ (class 1 = NO-Hardhat)
            helmet_results = helmet_model(frame, classes=[1], conf=0.3, imgsz=320, verbose=False)
            
            for box in helmet_results[0].boxes:
                hx1, hy1, hx2, hy2 = map(int, box.xyxy[0])
                cls_id = int(box.cls[0])
                class_name = helmet_model.names[cls_id]
                
                # Kiểm tra class vi phạm: NO-Hardhat (không mũ)
                is_violation_class = (class_name in ['NO-Hardhat', 'NO-Hardhat', 'no-helmet', 'without-helmet'])
                
                if is_violation_class:
                    # --- BƯỚC 3: Logic kết hợp ---
                    # Kiểm tra xem cái đầu này có nằm gần chiếc xe máy nào không
                    person_on_bike = False
                    for moto_box in motorcycles:
                        # Mở rộng vùng kiểm tra xe máy lên trên một chút (vì đầu người ở trên xe)
                        expanded_moto = [moto_box[0], moto_box[1] - 100, moto_box[2], moto_box[3]]
                        
                        if is_overlapping([hx1, hy1, hx2, hy2], expanded_moto):
                            person_on_bike = True
                            break
                    
                    if person_on_bike:
                        color = (0, 0, 255) # Đỏ (Vi phạm thật sự)
                        label = "VI PHAM"
                        violation_confirmed = True
                        # Vẽ khung đỏ quanh đầu
                        cv2.rectangle(frame, (hx1, hy1), (hx2, hy2), color, 2)
                        cv2.putText(frame, label, (hx1, hy1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                    else:
                        # Người đi bộ không đội nón -> Bỏ qua (Vẽ màu xám hoặc không vẽ)
                        pass

        # --- BƯỚC 4: Lưu ảnh toàn cảnh ---
        if violation_confirmed:
            current_time = time.time()
            if current_time - last_save_time > SAVE_COOLDOWN:
                filename = f"violation_{int(current_time)}.jpg"
                filepath = os.path.join(VIOLATION_DIR, filename)
                # Lưu nguyên khung hình (Toàn cảnh)
                cv2.imwrite(filepath, frame)
                print(f"📸 Đã chụp vi phạm xe máy: {filename}")
                last_save_time = current_time

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    try:
        images = sorted(os.listdir(VIOLATION_DIR), key=lambda x: os.path.getmtime(os.path.join(VIOLATION_DIR, x)), reverse=True)[:10]
    except:
        images = []
    return render_template('index.html', images=images, current_camera=current_camera)

@app.route('/debug')
def debug():
    """Trang debug để kiểm tra hệ thống"""
    return render_template('debug.html')

@app.route('/video_feed')
def video_feed():
    return Response(detect_and_process(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_available_cameras')
def get_available_cameras():
    """Lấy danh sách camera có sẵn"""
    available_cameras = []
    for i in range(5):  # Kiểm tra tối đa 5 camera (giảm để tránh lag)
        if i == current_camera:
            # Camera đang dùng - không test lại
            available_cameras.append({
                'index': i,
                'name': f'Camera {i} (Đang dùng)'
            })
            continue
        try:
            test_cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            if test_cap.isOpened():
                available_cameras.append({
                    'index': i,
                    'name': f'Camera {i}'
                })
                test_cap.release()
                time.sleep(0.2)  # Chờ camera giải phóng
        except:
            pass
    return jsonify(available_cameras)

@app.route('/change_camera', methods=['POST'])
def change_camera():
    """Đổi camera"""
    global current_camera
    data = request.get_json()
    camera_index = int(data.get('camera_index', 0))
    
    if init_camera(camera_index):
        current_camera = camera_index
        return jsonify({'success': True, 'message': f'Đã chuyển sang Camera {camera_index}'})
    else:
        return jsonify({'success': False, 'message': 'Không thể mở camera này'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
