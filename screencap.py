#!/bin/python3

#  from PIL import ImageGrab
import numpy as np
import cv2
import time
import board
import neopixel

'''
    strips must have the same number of leds on each side and on top and bottom
    should be linked in following order
    ________ 2 ________
    |                 |
                     
    3                 1
                     
    |                 |
    ________ 4 ________
'''
horizontalLEDs = 55 
verticalLEDs = 30

# adjust for the non-linear scaling of color
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

class tvBacklight:
    def __init__(self, status="off", brightness=100, mode="edge"):
        pixel_pin = board.D18 # pin 12 on rpi
        num_pixels = 2*horizontalLEDs + 2*verticalLEDs
        ORDER = neopixel.RGB

        self.blank = np.load("noConnection.npy")

        self.status = status
        self.brightness = brightness
        self.mode = mode

        # init and blank pixels
        self.pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER)
        self.pixels.fill((0,0,0))
        self.pixels.show()

        # init recording
        self.cap = cv2.VideoCapture(0)
        #  cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) # unnecessary, but my capture card is capable
        #  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        #  cap.set(cv2.CAP_PROP_FPS, 30)

        # chooses the pixels to look at 
        self.toWatch = self.getPixels(horizontalLEDs, verticalLEDs, self.mode)
        print("pixels", len(self.toWatch[0]), len(self.toWatch[1]))

    # sets every led to the same value
    def fill(self, tup):
        print('filling to', tup)
        self.pixels.fill(tup)
        self.pixels.show()

    def getFrame(self):
        ret, frame = self.cap.read()
        return frame

    # decides which pixels to get based on the number of leds and the resolution of the input
    def getPixels(self, horizontalLEDs, verticalLEDs, mode): # assumes same # on top and bottom
        if mode == "edge":
            f = self.getFrame()
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
    
    # gets the current frame and important pixels and sets the values of the leds accordingly
    def setLEDs(self): # make bottom right start of the chain going 
        
        screenPix = self.toWatch
        frame = self.getFrame()

        if not np.equal(frame, self.blank).all():
            print("in loop")
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
                
            # make everything fit in a counterclockwise circle starting bottom right
            #   same as pixart image above
            right.reverse()
            topRow.reverse()
            concatenatedList = np.concatenate((right, topRow, left, bottomRow))

            #  print(len(pixels), len(concatenatedList), "\n\n\n")
            # actually set the pixels from the combined list
            for i in range(0, len(concatenatedList)):
                t = concatenatedList[i]
                b, r, g = t
                b = gammaCorrection[b]
                r = gammaCorrection[r]
                g = gammaCorrection[g]

                self.pixels[i] = (r, g, b)
            
            self.pixels.show()
        else:
            self.fill((0,0,0))

    # clean up opencv
    def exit(self):
        self.cap.release()
        #  cv.destroyAllWindows()


if __name__ == "__main__":
    b = tvBacklight()

    while True:
        try:
            b.setLEDs()
        except KeyboardInterrupt:
            break

    print("exiting")
    b.fill((0,0,0))
    b.exit()
