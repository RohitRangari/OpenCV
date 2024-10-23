import cv2
from cvzone.FaceDetectionModule import FaceDetector
import webbrowser
import time
import keyboard

cap = cv2.VideoCapture(0)
detector = FaceDetector(minDetectionCon=0.8)  # Adjust detection confidence threshold

# State variable to track face detection
face_detected = False

while True:
    success, img = cap.read()
    img, bboxs = detector.findFaces(img)

    # Check if face is detected and trigger actions only once per detection
    if bboxs and not face_detected:
        webbrowser.open("https://blr1.blynk.cloud/external/api/update?token=cqud5NQ0y5DmjY2rxL6twtyWdkLjgRCj&v0=1")
        print("Face detected, sending ON link (1)")
        face_detected = True
        time.sleep(2)  # Adjust delay between detections
        # Close browser tab (optional)
        keyboard.press_and_release('ctrl + w')  # Uncomment if desired

    # Update state if no face is detected after a delay
    elif not bboxs and face_detected:
        webbrowser.open("https://blr1.blynk.cloud/external/api/update?token=cqud5NQ0y5DmjY2rxL6twtyWdkLjgRCj&v0=0")
        print("Face not detected, sending OFF link (0)")
        face_detected = False
        time.sleep(2)  # Adjust delay after no face detection
        keyboard.press_and_release('ctrl + w')  # Uncomment if desired

    
    cv2.imshow("Image", img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()