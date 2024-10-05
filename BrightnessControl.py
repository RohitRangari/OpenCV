import cv2 as cv #for computer vision tasks
import numpy as np #Used for numerical operations
import screen_brightness_control as scb #library to control the screen brightness
from cvzone.HandTrackingModule import HandDetector #Used to detect hands and track hand landmarks

# import pyvolume


cap = cv.VideoCapture(0) #Opens the webcam for capturing video
hd = HandDetector() #Initializes the hand detector to detect hands
val = 0 #Sets an initial value for the position of the brightness indicator rectangle 

while 1:
    _,img = cap.read() #Reads each frame from the webcam
    hands,img = hd.findHands(img) #Detects hands and adds visual markers
    # print(hands) #hands contains information of detected hand with landmark positions
    
    ''' 
    Hands contain 4 keys in their list 
    1. lmlist
    2. bbox
    3. center
    4. type 
    '''
    if hands: #if hands are detected
        
        lm = hands[0]['lmList'] #Extracts the landmark list 
        #print(lm) #list contains the coordinates of hand landmarks

        '''
        length: The distance between the two points.
        info: Extra information about the distance (like midpoint coordinates).
        img: The image with a visual representation of the distance.
        '''
        #Calculates distance between tip of index finger lm[8] & tip of thumb lm[4]
        length,info,img = hd.findDistance(lm[8][0:2],lm[4][0:2],img)
        # print(lenght)

        blevel = np.interp(length,[25,145],[0,100])
        val = np.interp(length, [0, 100],[400,150])
        blevel = int(blevel)
        # print(blevel)

        # Sets the screen brightness to the calculated blevel value
        scb.set_brightness(blevel)
        # pyvolume.custom(percent=blevel)

        # Draws an outline of a rectangle to represent the brightness level bar.
        cv.rectangle(img,(20,150),(85,400),(0,255,255),4)

        #Fills in the rectangle to visually indicate the current brightness level.
        cv.rectangle(img, (20, int(val)), (85, 400), (0, 0, 255), -1)

        # Puts text below the rectangle showing the current brightness percentage.
        cv.putText(img,str(blevel)+'%',(20,430),cv.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)

    cv.imshow('frame', img) #To display 
    if cv.waitKey(1) == ord('q'):
        break

cap.release() #Releases the webcam resource.
cv.destroyAllWindows() #Closes all OpenCV windows properly