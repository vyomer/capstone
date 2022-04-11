import time
import cv2
import numpy as np

fourcc = cv2.VideoWriter_fourcc(*'XVID')
outputfile = cv2.VideoWriter('output.avi',fourcc,20.0,(640,480))
caps = cv2.VideoCapture(0)
time.sleep(2)
bg = 0
for i in range(60):
    ret,bg = caps.read()
bg = np.flip(bg,axis = 1)
while(caps.isOpened()):
    ret,img = caps.read()
    if not ret:
        break
    img = np.flip(img,axis = 1)
    hsv = cv2.cvtColor(img,cv2.BGR2HSV)
    lowerred = np.arrey([0,120,50])
    upperred = np.arrey([10,255,255])
    mask1 = cv2.inRange(hsv,lowerred,upperred)
    lowerred = np.arrey([170,120,70])
    upperred = np.arrey([180,255,255])
    mask2 = cv2.inRange(hsv,lowerred,upperred)
    mask1 = mask1+mask2
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))
    mask2 = cv2.bitwise_not(mask1)
    result1 = cv2.bitwise_and(img,img,mask = mask2)
    result2 = cv2.bitwise_and(bg,bg,mask = mask1)
    final_output = cv2.addWeighted(result1,1,result2,1,0)
    outputfile.write(final_output)
    cv2.imshow("magic",final_output)
    cv2.waitKey(1)
caps.release()
#out.release()
cv2.destroyAllWindows()
