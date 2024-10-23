import cv2
from cvzone.HandTrackingModule import HandDetector
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# from ctypes import cast, POINTER
# from comtypes import CLSCTX_ALL
import numpy as np
import pyvolume
# Initialize video capture
cap = cv2.VideoCapture(0)

# Hand Detector with a confidence threshold of 0.8
detector = HandDetector(detectionCon=0.8, maxHands=1)

## Pycaw setup for volume control
# devices = AudioUtilities.GetSpeakers()
# interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
# volume = cast(interface, POINTER(IAudioEndpointVolume))

# # Get the volume range
# volRange = volume.GetVolumeRange()
# minVol = volRange[0]
# maxVol = volRange[1]

# Mapping function to convert finger count to volume
def finger_count_to_volume(fingers):
    volume_levels = {1: 0.2, 2: 0.4, 3: 0.6, 4: 0.8, 5: 1.0}
    return volume_levels.get(fingers, 0)

while True:
    # Capture frame from camera
    success, img = cap.read()

    # Detect hands in the frame
    hands, img = detector.findHands(img)

    if hands:
        # Get the number of raised fingers
        hand = hands[0]
        fingers = detector.fingersUp(hand)

        # Count raised fingers
        finger_count = fingers.count(1)

        # Convert finger count to volume
        target_volume = finger_count_to_volume(finger_count)
        pyvolume.custom(percent=int(target_volume * 100))
        # Set the system volume based on finger count
        # volume.SetMasterVolumeLevelScalar(target_volume, None)

        # Display finger count and volume on the frame
        cv2.putText(img, f'Volume: {int(target_volume * 100)}%', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

    # Display the resulting frame
    cv2.imshow("Hand Detection", img)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and destroy windows
cap.release()
cv2.destroyAllWindows()
