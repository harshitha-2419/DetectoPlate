import cv2
from plate_detection import detect_plate
from database_operations import get_car_details

def main(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Unable to open video file. Check the path!")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("End of video or error reading frame.")
            break

        plates = detect_plate(frame)
        for plate in plates:
            car_details = get_car_details(plate)
            print(f"Plate: {plate} - Details: {car_details}")

        cv2.imwrite("static/detected_frame.jpg", frame)  # Saves instead of showing
        break  # Stops after processing one frame (optional)

    cap.release()

# Example usage
if __name__ == "__main__":
    main("../static/sample_video.mp4")