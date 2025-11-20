"""
Tool test phát hiện không đội mũ bảo hiểm từ video file
Đặt video vào thư mục duan/ với tên: test.mp4
"""
import cv2
import time
from ultralytics import YOLO
import os

# Load models
print("Dang tai model...")
vehicle_model = YOLO('yolov8n.pt')
helmet_model = YOLO('best.pt')
print("Model da san sang!")

# Đường dẫn video
VIDEO_PATH = 'test.mp4'  # Đặt video vào cùng thư mục với file này

if not os.path.exists(VIDEO_PATH):
    print(f"KHONG TIM THAY VIDEO: {VIDEO_PATH}")
    print("Hay dat file video vao thu muc duan/ va dat ten la 'test.mp4'")
    input("Nhan Enter de thoat...")
    exit()

# Mở video
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    print("KHONG THE MO VIDEO!")
    exit()

# Thông tin video
fps = int(cap.get(cv2.CAP_PROP_FPS))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(f"\n{'='*50}")
print(f"VIDEO: {VIDEO_PATH}")
print(f"Kich thuoc: {width}x{height}")
print(f"FPS: {fps}")
print(f"Tong frames: {total_frames}")
print(f"Thoi luong: {total_frames/fps:.1f} giay")
print(f"{'='*50}\n")

# Tạo thư mục lưu vi phạm
os.makedirs('test_violations', exist_ok=True)

violation_count = 0
frame_count = 0
last_save_time = 0
SAVE_COOLDOWN = 2  # Lưu mỗi 2 giây

def is_overlapping(box1, box2):
    """Kiểm tra 2 box có chồng lấn không"""
    x_left = max(box1[0], box2[0])
    y_top = max(box1[1], box2[1])
    x_right = min(box1[2], box2[2])
    y_bottom = min(box1[3], box2[3])
    return not (x_right < x_left or y_bottom < y_top)

print("BAT DAU PHAN TICH VIDEO...")
print("Nhan 'q' de thoat | Nhan Space de tam dung\n")

start_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        print("\nDA PHAN TICH XONG VIDEO!")
        break
    
    frame_count += 1
    current_time = time.time()
    
    # Chỉ xử lý mỗi 2 frame
    if frame_count % 2 != 0:
        continue
    
    # --- BƯỚC 1: Tìm Xe Máy ---
    vehicle_results = vehicle_model(frame, classes=[3], conf=0.3, imgsz=320, verbose=False)
    
    motorcycles = []
    for box in vehicle_results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        motorcycles.append([x1, y1, x2, y2])
        # Vẽ khung xe máy
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 165, 255), 2)
        cv2.putText(frame, "Xe May", (x1, y1 - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)
    
    # --- BƯỚC 2: Tìm người không đội mũ ---
    violation_found = False
    
    if len(motorcycles) > 0:
        helmet_results = helmet_model(frame, classes=[1], conf=0.3, imgsz=320, verbose=False)
        
        for box in helmet_results[0].boxes:
            hx1, hy1, hx2, hy2 = map(int, box.xyxy[0])
            
            # Kiểm tra có trùng với xe máy không
            for mx1, my1, mx2, my2 in motorcycles:
                if is_overlapping([hx1, hy1, hx2, hy2], [mx1, my1, mx2, my2]):
                    # VI PHẠM!
                    violation_found = True
                    cv2.rectangle(frame, (hx1, hy1), (hx2, hy2), (0, 0, 255), 3)
                    cv2.putText(frame, "VI PHAM!", (hx1, hy1 - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    
                    # Lưu ảnh vi phạm
                    if current_time - last_save_time > SAVE_COOLDOWN:
                        violation_count += 1
                        filename = f'test_violations/vi_pham_{violation_count:03d}_frame_{frame_count}.jpg'
                        cv2.imwrite(filename, frame)
                        print(f"✓ VI PHAM #{violation_count} - Frame {frame_count} - Luu: {filename}")
                        last_save_time = current_time
                    break
    
    # Hiển thị thông tin
    progress = (frame_count / total_frames) * 100
    info_text = f"Frame: {frame_count}/{total_frames} ({progress:.1f}%) | Vi pham: {violation_count}"
    cv2.putText(frame, info_text, (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    if violation_found:
        cv2.putText(frame, "CANH BAO: PHAT HIEN VI PHAM!", (10, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    
    # Hiển thị frame
    cv2.imshow('Test Video - Phat hien khong doi mu', frame)
    
    # Xử lý phím
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        print("\nNGUNG PHAN TICH (nguoi dung yeu cau)")
        break
    elif key == ord(' '):
        print("TAM DUNG - Nhan Space de tiep tuc")
        cv2.waitKey(0)

# Kết thúc
elapsed = time.time() - start_time
cap.release()
cv2.destroyAllWindows()

print(f"\n{'='*50}")
print(f"KET QUA PHAN TICH")
print(f"{'='*50}")
print(f"Tong frames da xu ly: {frame_count}")
print(f"Tong vi pham phat hien: {violation_count}")
print(f"Thoi gian xu ly: {elapsed:.1f} giay")
print(f"Toc do xu ly: {frame_count/elapsed:.1f} FPS")
print(f"Anh vi pham luu tai: test_violations/")
print(f"{'='*50}\n")
