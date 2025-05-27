import cv2
import time
from plate_detection import detect_plate

def test_detect_plate():
    image_path = "static/sample_video1.mp4"  # Using a video frame might not work, better to use an image if available
    # Instead, read a frame from the video
    cap = cv2.VideoCapture(image_path)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        print("Failed to read frame from video")
        return

    start_time = time.time()
    plates = detect_plate(frame)
    end_time = time.time()

    print(f"Detected plates: {plates}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    test_detect_plate()
