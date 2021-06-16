#!/bin/python3


def videoTest():
    import cv2

    cap = cv2.VideoCapture(1)

    while(1):
        ret, frame = cap.read()
        cv2.imshow('Cam', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def rgbStripTest():
    import neopixel
    import board
    import time

    
    horizontalLEDs = 55
    verticalLEDs = 30


    pixel_pin = board.D18
    num_pixels = 2*horizontalLEDs + 2*verticalLEDs
    ORDER = neopixel.RGB

    pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER)
    pixels.fill((255,255,255))
    pixels.show()
    #  time.sleep(1)
    #  pixels.fill((0,255,0))
    #  pixels.show()
    #  time.sleep(1)
    #  pixels.fill((0,0,255))
    #  pixels.show()
    #  time.sleep(1)
    #  pixels.fill((0,0,0))


#  rgbStripTest()
videoTest()
