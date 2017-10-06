# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
#from django.template import loader
from django.shortcuts import render

from sensor.DHTSensor import DHTSensor as Sensor
from relais.Relais import Relais
import threading
from Lock import *

FILEPATH = "/home/pi/"

# Create your views here.
def index(request):
    return status(request, "", "")


def windowProcess(action):
    print("process started %s" % action)
    r = Relais(17, 22)
    r.setAction(action)
    print r
    r.run()
    print("process finished")


def measure(request):
    sensorOut = Sensor(15, 'DHT22', True)
    sensorOut.readTemp()
    
    sensorIn = Sensor(14, 'DHT11', True)
    sensorIn.readTemp()
    return render(request, 'templates/window/measure.html', {})


def info(request):
    # tmp
    sensorOut = Sensor(15, 'DHT22')
    sensorOut.readFromFile()
    
    sensorIn = Sensor(14, 'DHT11')
    sensorIn.readFromFile()

    # windowState
    windowState = "unknown"
    f = open("%s./windowStatus" % FILEPATH, "r")
    if f:
        windowState = f.readline()
        f.close()

    context = {
        'where' : id,
        'tempOut' : sensorOut.readFromFile(),
        'tempIn' : sensorIn.readFromFile(),
        'windowState': windowState
    }
    return render(request, 'templates/window/info.html', context)
    

def action(request, action = "" ):
    # relais
    if action != "":
        t = threading.Thread(target=windowProcess, args=(action,), kwargs={})
        t.setDaemon(True)
        t.start()
    
    context = {}
    return render(request, 'templates/window/action.html', context)
    
