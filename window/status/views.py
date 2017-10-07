# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
#from django.template import loader
from django.shortcuts import render

from sensor.DHTSensor import DHTSensor as Sensor
from relais.Relais import Relais
import threading
from Lock import *
from django.utils import timezone
from .models import Temperature

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
    
    tIn = Temperature(temp_value=sensorIn.getTemperature(),temp_type="in",pub_date=timezone.now())
    tIn.save()

    tOut = Temperature(temp_value=sensorOut.getTemperature(),temp_type="out",pub_date=timezone.now())
    tOut.save()

    return render(request, 'templates/window/measure.html', {})


def info(request):
    # tmp
    all = Temperature.objects.all().order_by('-pub_date')
    tempIn = Temperature.objects.filter(temp_type__lte='in').order_by('-pub_date')[0]
    tempOut = Temperature.objects.filter(temp_type__lte='out').order_by('-pub_date')[0]

    # windowState
    windowState = "unknown"
    f = open("%s./windowStatus" % FILEPATH, "r")
    if f:
        windowState = f.readline()
        f.close()

    context = {
        'where' : id,
        'entries': all,
        'tempOut' : tempOut,
        'tempIn' : tempIn,
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
    
