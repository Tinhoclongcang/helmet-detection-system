"""
Flask App - Upload Video và Phát Hiện Vi Phạm Không Đội Mũ Bảo Hiểm
Dành cho deploy lên Render.com hoặc các nền tảng cloud
"""
import cv2
import os
import time
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from ultralytics import YOLO
import threading

app = Flask(__name__)

# --- CẤU HÌNH ---
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/video_violations'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}

# Tạo thư mục nếu chưa có
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # Max 500MB

# Load Models
print("🤖 Đang tải AI models...")
try:
    vehicle_model = YOLO('yolov8n.pt')
    helmet_model = YOLO('best.pt')
    print("✅ Models đã sẵn sàng!")
except Exception as e:
    print(f"❌ Lỗi tải models: {e}")
    vehicle_model = None
    helmet_model = None

# Lưu trạng thái xử lý video
processing_status = {}

def allowed_file(filename):
    """Kiểm tra file có hợp lệ không"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_overlapping(box1, box2):
    """Kiểm tra 2 box có chồng lấn không"""
    x_left = max(box1[0], box2[0])
    y_top = max(box1[1], box2[1])
    x_right = min(box1[2], box2[2])
    y_bottom = min(box1[3], box2[3])
    return not (x_right < x_left or y_bottom < y_top)

def process_video_file(video_path, session_id):
    """Xử lý video và phát hiện vi phạm"""
    global processing_status
    
    try:
        # Cập nhật trạng thái
        processing_status[session_id] = {
            'status': 'processing',
            'progress': 0,
            'violations': [],
            'total_frames': 0,
            'processed_frames': 0,
            'message': 'Đang khởi tạo...'
        }
        
        # Mở video
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            processing_status[session_id]['status'] = 'error'
            processing_status[session_id]['message'] = 'Không thể mở video'
            return
        
        # Thông tin video
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        processing_status[session_id]['total_frames'] = total_frames
        processing_status[session_id]['video_info'] = {
            'fps': fps,
            'width': width,
            'height': height,
            'duration': f"{total_frames/fps:.1f}s"
        }
        
        # Tạo thư mục riêng cho session
        session_output = os.path.join(OUTPUT_FOLDER, session_id)
        os.makedirs(session_output, exist_ok=True)
        
        violation_count = 0
        frame_count = 0
        last_save_time = 0
        SAVE_COOLDOWN = 2  # Lưu mỗi 2 giây
        
        processing_status[session_id]['message'] = 'Đang phân tích video...'
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            processing_status[session_id]['processed_frames'] = frame_count
            processing_status[session_id]['progress'] = int((frame_count / total_frames) * 100)
            
            # Chỉ xử lý mỗi 2 frame để tăng tốc
            if frame_count % 2 != 0:
                continue
            
            current_time = time.time()
            
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
                        # Mở rộng vùng xe máy lên trên
                        expanded_moto = [mx1, my1 - 100, mx2, my2]
                        
                        if is_overlapping([hx1, hy1, hx2, hy2], expanded_moto):
                            # VI PHẠM!
                            violation_found = True
                            cv2.rectangle(frame, (hx1, hy1), (hx2, hy2), (0, 0, 255), 3)
                            cv2.putText(frame, "VI PHAM!", (hx1, hy1 - 10), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                            
                            # Lưu ảnh vi phạm
                            if current_time - last_save_time > SAVE_COOLDOWN:
                                violation_count += 1
                                filename = f'violation_{violation_count:03d}_frame_{frame_count}.jpg'
                                filepath = os.path.join(session_output, filename)
                                cv2.imwrite(filepath, frame)
                                
                                # Lưu thông tin vi phạm
                                processing_status[session_id]['violations'].append({
                                    'id': violation_count,
                                    'frame': frame_count,
                                    'time': f"{frame_count/fps:.1f}s",
                                    'image': f"{session_id}/{filename}"
                                })
                                
                                last_save_time = current_time
                            break
            
            # Cập nhật message
            if frame_count % 30 == 0:  # Cập nhật mỗi 30 frames
                processing_status[session_id]['message'] = f'Đang xử lý frame {frame_count}/{total_frames} - Phát hiện {violation_count} vi phạm'
        
        cap.release()
        
        # Hoàn thành
        processing_status[session_id]['status'] = 'completed'
        processing_status[session_id]['progress'] = 100
        processing_status[session_id]['message'] = f'Hoàn thành! Phát hiện {violation_count} vi phạm'
        processing_status[session_id]['violation_count'] = violation_count
        
    except Exception as e:
        processing_status[session_id]['status'] = 'error'
        processing_status[session_id]['message'] = f'Lỗi xử lý: {str(e)}'
        print(f"❌ Lỗi xử lý video: {e}")

@app.route('/')
def upload_page():
    """Trang upload video"""
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    """API upload video"""
    if 'video' not in request.files:
        return jsonify({'success': False, 'message': 'Không có file được chọn'}), 400
    
    file = request.files['video']
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'Không có file được chọn'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'Định dạng file không hợp lệ. Chỉ chấp nhận: mp4, avi, mov, mkv, webm'}), 400
    
    if vehicle_model is None or helmet_model is None:
        return jsonify({'success': False, 'message': 'AI Models chưa sẵn sàng. Vui lòng thử lại sau.'}), 500
    
    try:
        # Lưu file
        filename = secure_filename(file.filename)
        session_id = f"session_{int(time.time())}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}_{filename}")
        file.save(file_path)
        
        # Bắt đầu xử lý video trong thread riêng
        thread = threading.Thread(target=process_video_file, args=(file_path, session_id))
        thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Upload thành công. Đang xử lý video...',
            'session_id': session_id
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Lỗi upload: {str(e)}'}), 500

@app.route('/status/<session_id>')
def get_status(session_id):
    """API lấy trạng thái xử lý"""
    if session_id not in processing_status:
        return jsonify({'status': 'not_found', 'message': 'Session không tồn tại'}), 404
    
    return jsonify(processing_status[session_id])

@app.route('/results/<session_id>')
def view_results(session_id):
    """Trang hiển thị kết quả"""
    if session_id not in processing_status:
        return "Session không tồn tại", 404
    
    return render_template('results.html', 
                         session_id=session_id,
                         status=processing_status[session_id])

@app.route('/static/video_violations/<path:filename>')
def serve_violation_image(filename):
    """Serve ảnh vi phạm"""
    return send_from_directory(OUTPUT_FOLDER, filename)

@app.route('/health')
def health_check():
    """Health check cho Render.com"""
    return jsonify({
        'status': 'ok',
        'models_loaded': vehicle_model is not None and helmet_model is not None,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
