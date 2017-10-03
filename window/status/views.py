# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse

from sensor.DHTSensor import DHTSensor as Sensor

# Create your views here.
def index(request):
    return HttpResponse("index")

def status(request, id):
    if ( id == "out"):
        sensor = Sensor(14, 'DHT11', True)
    else:
        sensor = Sensor(15, 'DHT22', True)

    sensor.readTemp()
    return HttpResponse("temperatur %s = %f Grad" % (id, sensor.getTemperature()))

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)