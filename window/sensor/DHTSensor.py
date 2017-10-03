#!/usr/bin/python
# coding=utf-8

import RPi.GPIO as GPIO
import Adafruit_DHT
from time import gmtime, strftime


class DHTSensor(object):

    allowedSensorTypes  = ['DHT11', 'DHT22']
    sensorType          = 'DHT11'
    pin                 = 14
    DEBUG               = False
    currentTemp         = None
    temperature          = -100.0
    hasSensorReadError  = False
    tempDelta       = 0.5
    hasDeltaChange      = False

    """
    """
    def __init__(self, pin, sensorType = 'DHT11', debug = False):
        if pin is None:
            raise Exception('Pin required')

        if sensorType not in self.allowedSensorTypes:
            raise Exception('SensorType %s is not allowed' % sensorType)

        self.sensorType = Adafruit_DHT.DHT11
        if sensorType == 'DHT22': self.sensorType = Adafruit_DHT.DHT22

        self.pin = pin
        self.DEBUG = debug

    """
    """
    def readFromSensor(self):
        self.hasSensorReadError = True  # default

        humidity, temp = Adafruit_DHT.read_retry(self.sensorType, self.pin)

        if temp is None: raise Exception()

        self.currentTemp = temp
        self.hasSensorReadError = False


    """
    """
    def readTemp(self):
        # try reading from sensor (max. 3 times)
        count = 0
        while count < 3 :
            count += 1
            try:
                self.readFromSensor()
            except Exception:
                self.debug('DHT%s - Fehler beim Auslesen... Starte neu ...' % self.sensorType)
                time.sleep(2)  # sensor need some surcease

        self.debug(self)

    """
    """
    def debug(self, msg):
        if self.DEBUG is False: return ''
        print msg

    """
    """
    def __str__(self):
        msg = ""
        msg += "\tSensorType: DHT-%s\n" % self.sensorType
        msg += "\tTemperatur: %2.2f °C\n" % self.getTemperature()
        return msg

    def getTemperature(self):
        return self.currentTemp

if __name__ == '__main__':
    import time

    try:
        #d11 = DHTSensor(14, 'DHT11', True)
        d22 = DHTSensor(15, 'DHT22', True)
        while True:
            #d11.readTemp()
            #print d11
            d22.readTemp()
            print d22
            time.sleep(5)
    except KeyboardInterrupt:
        print "done"