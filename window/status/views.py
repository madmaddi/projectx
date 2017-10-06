# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
#from django.template import loader
from django.shortcuts import render

from sensor.DHTSensor import DHTSensor as Sensor
from relais.Relais import Relais
import threading
from Lock import *

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

def measureProcess(id):
    print("process started %s" % id)
    if id == "out":
        sensor = Sensor(15, 'DHT22', True)
    else:
        sensor = Sensor(14, 'DHT11', True)

    #sensor.readTemp()
    sensor.run()
    print("process finished")

def status(request, id = "", action =""):
    # tmp
    measure = threading.Thread(target=measureProcess, args=(id,), kwargs={})
    measure.setDaemon(True)
    measure.start()

    # relais
    if action != "":
        t = threading.Thread(target=windowProcess, args=(action,), kwargs={})
        t.setDaemon(True)
        t.start()

    # windowState
    windowState = "unknown"
    f = open("/tmp/windowStatus", "r")
    if f:
        windowState = f.readline()
        f.close()

    context = {
        'where' : id,
        'temp' : "sensor.readFromFile()",
        'windowState': windowState
    }
    return render(request, 'templates/window/index.html', context)
    
