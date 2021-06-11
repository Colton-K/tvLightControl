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

gammaCorrection = [
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
    1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
    2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
    5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
    10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
    17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
    25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
    37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
    51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
    69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
    90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
    115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
    144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
    177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
    215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255
]



pixel_pin = board.D18

num_pixels = 2*horizontalLEDs + 2*verticalLEDs
#  ORDER = neopixel.GRB
ORDER = neopixel.RGB
#  ORDER = neopixel.GBR

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER)
pixels.fill((0,0,0))
pixels.show()

cap = cv2.VideoCapture(0)
#  cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
#  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)


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
    print("Resolution:",resolution)

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
    resolution = len(frame[0]), len(frame) # width, height ex (1920, 1080)
    topRow = []
    bottomRow = []
    left = []
    right = []

    xPix, yPix = screenPix 
    for p in xPix:
        topRow.append(frame[0][p])
        bottomRow.append(frame[resolution[1]-1][p])

    for p in yPix:
        left.append(frame[p][0])
        right.append(frame[p][resolution[0]-1])
        
        #  print(p, len(screenPix[0])-1, xPix[-1])
        #  print(xPix)

    #  print(topRow)
    #  print(bottomRow)
    #  print(left, "----------------------------")
    #  print(right, "\n\n\n")

    # make everything fit in a counterclockwise circle starting bottom right
    right.reverse()
    topRow.reverse()
    concatenatedList = np.concatenate((right, topRow, left, bottomRow))

    #  print(len(pixels), len(concatenatedList), "\n\n\n")
    for i in range(0, len(concatenatedList)):
        #  print(i, pixels[i], concatenatedList[i])
        t = concatenatedList[i]
        b, r, g = t
        b = gammaCorrection[b]
        r = gammaCorrection[r]
        g = gammaCorrection[g]

        #  print(r, g, b)
        pixels[i] = (r, g, b)
        #  pixels[i] = (0,0,0)
    
    pixels.show()

    #  print(type(concatenatedList))




toWatch = getImportantPixels(horizontalLEDs, verticalLEDs)
print("pixels", len(toWatch[0]), len(toWatch[1]))
while True:
    setLEDs(toWatch, getFrame())


cap.release()
cv2.destroyAllWindows()
