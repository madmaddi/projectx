#!/usr/bin/python
# coding=utf-8

import RPi.GPIO as GPIO
import time

from status.Singleton import Singleton
from status.config import OPEN_CLOSE_TIME

class Relais(object):
    __metaclass__ = Singleton

    pin1 = 17
    pin2 = 22
    delay = 5
    isConnectedThrough = False
    hasError = False
    action = "open"
    isRunning = False

    def __init__(self, pin1, pin2, delay = OPEN_CLOSE_TIME):
        if pin1 is None or pin2 is None:
            raise Exception('Pin required')

        self.pin1 = pin1
        self.pin2 = pin2
        self.delay = delay
        self.initGPIO()

    def setAction(self, action):
        self.action = action

    def initGPIO(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.pin1, GPIO.OUT)
        GPIO.output(self.pin1, False)
        GPIO.setup(self.pin2, GPIO.OUT)
        GPIO.output(self.pin2, False)

    def run(self):
        if self.action == "open":
            self.switch(self.pin1)
        else:
            self.switch(self.pin2)

    def switch(self, p):
        try:
            if self.isRunning:
                return

            self.isRunning = True
            self.stopAll()
            GPIO.output(p, True)  # connect through
            time.sleep(self.delay)  # wait n seconds
            GPIO.output(p, False)  # stop circuit connection
        except KeyboardInterrupt:
            raise
        except:
            GPIO.output(p, False)
            self.isRunning = False

        GPIO.output(p, False)
        self.isRunning = False

    def stopAll(self):
        try:
            # stop circuit connection
            GPIO.output(self.pin1, False)
            GPIO.output(self.pin2, False)
        except:
            import sys
            sys.exit(1)

if __name__ == '__main__':

    import sys

    print 'Argument List:', str(sys.argv)
    if len(sys.argv) < 2:
        print "cmd line arguments missed"
        sys.exit(1)

    arg1 = sys.argv[1]

    r = Relais(17, 22, arg1)
    r.start()
