#!/bin/python3

from PIL import ImageGrab
import numpy as np
import cv2


def getFrame():
    img = ImageGrab.grab(bbox=(0,0,1920,1080)) #bbox specifies specific region (bbox= x,y,width,height *starts top-left)
    img_np = np.array(img) #this is the array obtained from conversion
    frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    #  cv2.imshow("test", frame)
    #  cv2.waitKey(0)
    #  cv2.destroyAllWindows()
    return frame


def getImportantPixels(horizontalLEDs, verticalLEDs): # assumes same # on top and bottom
    f = getFrame()
    resolution = len(f[0]), len(f) # width, height ex (1920, 1080)

    horizontalStep = int(resolution[0] / horizontalLEDs)
    xPixels = []
    for i in range(0, resolution[0], horizontalStep):
        xPixels.append(i)

    verticalStep = int(resolution[1] / verticalLEDs)
    yPixels = []
    for i in range(0, resolution[1], verticalStep):
        yPixels.append(i)

    #  print(xPixels)
    #  print(yPixels)

    return xPixels, yPixels
    

def setLEDs(pixels, frame): # make bottom right start of the chain going 
    topRow = []
    bottomRow = []
    left = []
    right = []

    xPix, yPix = pixels
    for p in xPix:
        topRow.append(frame[0][p])
        bottomRow.append(frame[len(pixels)-1][p])

    for p in yPix:
        left.append(frame[p][0])
        right.append(frame[p][len(pixels[0])-1])

    #  print(topRow)
    #  print(bottomRow)
    #  print(left)
    #  print(right)

    # make everything fit in a counterclockwise circle starting bottom right
    right.reverse()
    topRow.reverse()

    concatenatedList = right + topRow + left + bottomRow

    print(concatenatedList)




toWatch = getImportantPixels(50, 16)
setLEDs(toWatch, getFrame())

