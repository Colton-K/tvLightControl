#!/bin/python3

#  from PIL import ImageGrab
import numpy as np
import cv2
import time
import board
import neopixel

'''
define theseeeeee
'''
horizontalLEDs = 55
verticalLEDs = 30


pixel_pin = board.D18
num_pixels = 2*horizontalLEDs + 2*verticalLEDs
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER)
pixels.fill((0,0,0))
pixels.show()

cap = cv2.VideoCapture(0)

def getFrame():
    #  img = ImageGrab.grab(bbox=(0,0,1920,1080)) #bbox specifies specific region (bbox= x,y,width,height *starts top-left)
    #  img_np = np.array(img) #this is the array obtained from conversion
    #  frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    ret, frame = cap.read()
    #  cv2.imshow("test", frame)
    #  cv2.waitKey(0)
    #  cv2.destroyAllWindows()
    return frame


def getImportantPixels(horizontalLEDs, verticalLEDs): # assumes same # on top and bottom
    f = getFrame()
    resolution = len(f[0]), len(f) # width, height ex (1920, 1080)

    horizontalStep = (resolution[0] / horizontalLEDs)
    xPixels = []
    i = 0
    while i < resolution[0]-1:
        xPixels.append(int(i))
        i += horizontalStep

    #  print(len(xPixels))

    verticalStep = int(resolution[1] / verticalLEDs)
    yPixels = []
    i = 0
    while i < resolution[1]-1:
        yPixels.append(i)
        i += verticalStep

    #  print(xPixels)
    #  print(yPixels)

    return xPixels, yPixels
    

def setLEDs(screenPix, frame): # make bottom right start of the chain going 
    topRow = []
    bottomRow = []
    left = []
    right = []

    xPix, yPix = screenPix 
    for p in xPix:
        topRow.append(frame[0][p])
        bottomRow.append(frame[len(screenPix)-1][p])

    for p in yPix:
        left.append(frame[p][0])
        right.append(frame[p][len(screenPix[0])-1])

    #  print(topRow)
    #  print(bottomRow)
    #  print(left)
    #  print(right)

    # make everything fit in a counterclockwise circle starting bottom right
    right.reverse()
    topRow.reverse()
    concatenatedList = np.concatenate((left, bottomRow, right, topRow))

    #  print(len(pixels), len(concatenatedList), "\n\n\n")
    for i in range(0, len(concatenatedList)):
        #  print(i, pixels[i], concatenatedList[i])
        pixels[i] = concatenatedList[i]
    
    pixels.show()

    #  print(type(concatenatedList))




toWatch = getImportantPixels(horizontalLEDs, verticalLEDs)
print("pixels", len(toWatch[0]), len(toWatch[1]))
while True:
    setLEDs(toWatch, getFrame())


cap.release()
cv2.destroyAllWindows()
