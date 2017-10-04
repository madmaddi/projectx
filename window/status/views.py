# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
#from django.template import loader
from django.shortcuts import render

from sensor.DHTSensor import DHTSensor as Sensor

# Create your views here.
def index(request):
    return HttpResponse("index")

def status(request, id = "", action =""):
    if ( id == "out"):
        sensor = Sensor(14, 'DHT11', True)
    else:
        sensor = Sensor(15, 'DHT22', True)

    sensor.readTemp()
    
    context = {
        'wo' : id,
        'temp' : sensor.readFromFile()
    }
    return render(request, 'templates/window/index.html', context)
    
