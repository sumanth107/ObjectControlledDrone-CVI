import cv2 as cv
import numpy as np
import rospy
from geometry_msgs.msg import PoseStamped

midpoint = PoseStamped()

cap = cv.VideoCapture(0) #replace video name with '0' to get real time detection
lower = np.array([134,80,80])  #hsv limits vary based on landing platform
upper = np.array([178,225,255])
rospy.init_node('todrone', anonymous=True)
publisher=rospy.Publisher('cv_bounding_box', PoseStamped,queue_size=20)

while True:
    ret, frame = cap.read()
    frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(frame_HSV, lower, upper)
    mask_Open = cv.morphologyEx(mask, cv.MORPH_OPEN, np.ones((10, 10)))
    mask_Close = cv.morphologyEx(mask_Open, cv.MORPH_CLOSE, np.ones((20, 20))) #to reduce noise and get smooth image
    mask_Perfect = mask_Close
    conts, h = cv.findContours(mask_Perfect.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE) # detects contours
    for c in conts:  #creates bounding boxes around the detected objects
        # Find the index of the largest contour
        areas = [cv.contourArea(c) for c in conts] 
        max_index = np.argmax(areas)
        cnt=conts[max_index]
        x, y, w, h = cv.boundingRect(cnt)
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv.circle(frame, (x + int(w*0.5), y + int(h*0.5)), 4, (0,0,255), -1) #locates the center of bounding box
        print(x + int(w * 0.5), y + int(h * 0.5))  #center of the bounding box
        midpoint.pose.position.x=x + int(w * 0.5)
        midpoint.pose.position.y=y + int(h * 0.5)
        midpoint.pose.position.z=0
        publisher.publish(midpoint)
    
    cv.imshow('boxred', frame)


    if cv.waitKey(1) & 0xFF == 27: #escape key to exit
        break
cap.release()
cv.destroyAllWindows()
