from flask import Flask, request, render_template, jsonify
import os
import cv2
from werkzeug.utils import secure_filename
from scripts.plate_detection import detect_plate
from scripts.database_operations import get_car_details

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Upload endpoint called")
    if 'video' not in request.files:
        return jsonify({'error': 'No video part'}), 400
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        cap = cv2.VideoCapture(filepath)
        detected_info = {}
        frame_count = 0
        max_frames = 10  # Limit to first 10 frames for performance
        frame_skip = 30  # Process every 30th frame

        while cap.isOpened() and frame_count < max_frames:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % frame_skip == 0:
                plates = detect_plate(frame)
                logging.debug(f"Frame {frame_count}: Detected plates: {plates}")
                for plate in plates:
                    if plate not in detected_info:
                        details = get_car_details(plate)
                        if details == "No details found.":
                            detected_info[plate] = "Details not found"
                        else:
                            detected_info[plate] = {
                                'Plate': details[0],
                                'Owner': details[1],
                                'Model': details[2],
                                'Color': details[3]
                            }
            frame_count += 1

        cap.release()
        os.remove(filepath)

        if not detected_info:
            detected_info = ["No license plates detected in the video."]
        else:
            formatted_results = []
            for plate, details in detected_info.items():
                if isinstance(details, str):
                    formatted_results.append(f"{plate} - {details}")
                else:
                    formatted_results.append(f"{plate} - Owner: {details['Owner']}, Model: {details['Model']}, Color: {details['Color']}")
            detected_info = formatted_results

        logging.debug("Returning detected info")
        return jsonify(detected_info)
    else:
        return jsonify({'error': 'File type not allowed'}), 400

if __name__ == '__main__':
    app.run(debug=True)
