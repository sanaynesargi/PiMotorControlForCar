#!/usr/bin/python3

from flask import Flask, request
from threading import Thread
import subprocess
import RPi.GPIO as GPIO
import time, sys, os

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


FIRST_CONTROL_PINS = [21, 26, 12, 6]
SECOND_CONTROL_PINS = [5, 20, 16, 19]

call = subprocess.Popen("hostname -I", shell=True, stdout=subprocess.PIPE)
IP_ADDRESS = call.stdout.read()
IP_ADDRESS = ''.join(list(str(IP_ADDRESS))[2:-4])


def up():
    stop()
    for pin in FIRST_CONTROL_PINS:
        GPIO.output(pin, True)

def down():
    stop()
    for pin in SECOND_CONTROL_PINS:
        GPIO.output(pin, True)

def right():
    stop()
    #GPIO.output(6, True)
    GPIO.output(26, True)
    GPIO.output(20, True)
    GPIO.output(16, True)

def left():
    stop()
    #GPIO.output(5, True)
    GPIO.output(19, True)
    GPIO.output(21, True)
    GPIO.output(12, True)

def stop():
    for f in FIRST_CONTROL_PINS:
        GPIO.output(f, False)

    for f in SECOND_CONTROL_PINS:
        GPIO.output(f, False)

def main():
    
    #os.system("sudo python3 /home/pi/kill_host_problems.py")
    for f in FIRST_CONTROL_PINS:
        GPIO.setup(f, GPIO.OUT)
        #GPIO.output(f, True) 
    for f in SECOND_CONTROL_PINS:
        GPIO.setup(f, GPIO.OUT)
        #GPIO.output(f, True)
    stop()
    #left()
    #GPIO.output(12, True)
    #GPIO.output(6, True)
    #GPIO.output(21, True)
    #GPIO.output(26, True)

def start_stream():
    os.system("sudo python3 /home/pi/kill_cam_problems.py")
    os.system("bash /home/pi/Downloads/start-stream.sh")
    
app = Flask(__name__)
@app.route('/', methods=['POST'])
def handle_request():
    if request.headers['dir'] == 'up':
         up()
         return 'going forward'
    if request.headers['dir'] == 'down':
        down()
        return 'going backward'
    if request.headers['dir'] == 'right':
        right()
        return 'turning right'
    if request.headers['dir'] == 'left':
        left()
        return 'turning left'
    if request.headers['dir'] == 'stop':
        stop()
        return 'stopped'

if __name__ == '__main__':
    t = Thread(target=start_stream, args=())
    t.start()
    main()
    app.run(host=IP_ADDRESS, port=8080)
