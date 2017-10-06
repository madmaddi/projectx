#!/usr/bin/python
# coding=utf-8

import RPi.GPIO as GPIO
import time

class Singleton(type):
    def __init__(self, name, bases, dict):
        super(Singleton, self).__init__(name, bases, dict)
        self.instance = None

    def __call__(self, *args, **kw):
        if self.instance is None:
            self.instance = super(Singleton, self).__call__(*args, **kw)

        return self.instance


class Relais(object):
    __metaclass__ = Singleton

    pin1 = 17
    pin2 = 22
    delay = 5
    isConnectedThrough = False
    hasError = False
    action = "open"
    isRunning = False

    def __init__(self, pin1, pin2, delay = 10):
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
        #print "Starte %s" % "self.name"
        if self.action == "open":
            self.switch(self.pin1)
        else:
            self.switch(self.pin2)
        #print "     Beende %s" % "self.name"

    def switch(self, p):
        try:
            if self.isRunning:
                #print "noch aktiv"
                return

            #print "läuft gerade"
            self.isRunning = True
            self.stopAll()
            GPIO.output(p, True)  # connect through
            time.sleep(self.delay)  # wait n seconds
            GPIO.output(p, False)  # stop circuit connection
            self.writeStatus(p)
        except KeyboardInterrupt:
            raise
        except:
            GPIO.output(p, False)
            self.isRunning = False


        GPIO.output(p, False)
        self.isRunning = False
        #print "     fertig"


    def writeStatus(self, p):
        f = open("/tmp/windowStatus", "w")
        status = "closed"
        if ( p == 17): status = "open" # todo p == 17 not hardcoded
        f.write(status)
        f.close()

    def stopAll(self):
        try:
            # stop circuit connection
            GPIO.output(self.pin1, False)
            GPIO.output(self.pin2, False)
            #time.sleep(self.delay/100)
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
    """
    l =[]
    for i in range(1,11):
        l.append(Relais(17, 22, lock,  i))

    for r in l:
        r.start()
    """