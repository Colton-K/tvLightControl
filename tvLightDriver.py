#!/bin/python3

from flask import Flask
import os
import socket

from screencap import tvBacklight

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

'''
    make the rgb strips accessible to set different colors as well if the system is off
        3 states - on, off, static
        static mode can either be synced with rest of the room or independent
'''

if __name__ == "__main__":
    app.run(host=getIP(), port=5000)
