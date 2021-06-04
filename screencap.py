#!/bin/python3

from PIL import ImageGrab
import numpy as np
import cv2

while True:
    img = ImageGrab.grab(bbox=(0,0,1920,1080)) #bbox specifies specific region (bbox= x,y,width,height *starts top-left)
    img_np = np.array(img) #this is the array obtained from conversion
    frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    #  cv2.imshow("test", frame)
    #  cv2.waitKey(0)
    #  cv2.destroyAllWindows()

    print(frame[0][0])
