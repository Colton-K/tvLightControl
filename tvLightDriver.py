#!/bin/python3

from flask import Flask, request
import os
import socket

import board
import neopixel
horizontalLEDs = 55 
verticalLEDs = 30

app = Flask(__name__)


def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        s.connect(("10.255.255.255", 1))
        IP = s.getsockname()[0]
    except:
        IP = "127.0.0.1"
    finally:
        s.close
    return IP

@app.route("/")
def index():
    return "hello"

@app.route("/on")
def on():
    os.system("systemctl start tvLights.service")
    return "on"

@app.route("/off")
def off():
    os.system("systemctl stop tvLights.service")
    return "off"

@app.route("/color", methods=["POST", "GET"])
def color():
    os.system("systemctl stop tvLights.service")
    
    if request.method == "POST":
        r = request.form["r"]
        g = request.form["g"]
        b = request.form["b"]
    else:
        r = request.args.get("r")
        g = request.args.get("g")
        b = request.args.get("b")

    if r is None:
        r = 0
    else:
        r = int(r)
    if g is None:
        g = 0
    else:
        g = int(g)
    if b is None:
        b = 0
    else:
        b = int(b)

    pixel_pin = board.D18 # pin 12 on rpi
    num_pixels = 2*horizontalLEDs + 2*verticalLEDs
    ORDER = neopixel.RGB
    pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER)
    pixels.fill((g,r,b))
    pixels.show()

    return f"{r},{g},{b}"

'''
    make the rgb strips accessible to set different colors as well if the system is off
        3 states - on, off, static
        static mode can either be synced with rest of the room or independent
'''

if __name__ == "__main__":
    app.run(host=getIP(), port=5000)
