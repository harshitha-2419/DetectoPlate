import cv2
import easyocr

reader = easyocr.Reader(['en'])

def detect_plate(frame):
    plate_text = reader.readtext(frame)

    detected_plates = []
    for detection in plate_text:
        detected_plates.append(detection[1])

    return detected_plates

# Example usage (used inside video processing script)
if __name__ == "__main__":
    frame = cv2.imread("static/test_plate.jpg")
    print("Detected License Plates:", detect_plate(frame))