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
from .models import Temperature, Window

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

from .serializer import TemperatureSerializer, WindowSerializer

FILEPATH = "/home/pi/"

@api_view(['GET'])
def windowState(request):
    if request.method == 'GET':
        snippet = Window.objects.order_by('-pubDate')[0]
        serializer = WindowSerializer(snippet)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def tempList(request, key = None, format = None):
    limit =  request.query_params.get('limit')
    if limit == None or limit == "": limit = 2000

    if request.method == 'GET':
        location = request.query_params.get('location')
        if location != None:
            snippets = Temperature.objects.filter(location=location).order_by('-pubDate')[:limit]
        else:
            snippets = Temperature.objects.order_by('-pubDate')[:limit]

        serializer = TemperatureSerializer(snippets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TemperatureSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def tempDetail(request, key, format = None):
    try:
        snippet = Temperature.objects.get(id = key)
    except Temperature.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TemperatureSerializer(snippet)
        return Response(serializer.data)


    elif request.method == 'PUT':
        serializer = TemperatureSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def action(request, action = "" ):
    if action == "":
        return Response({"status": "Fail, no action"})


    r = Relais(17, 22)
    isRunning = r.isRunning

    # relais
    t = threading.Thread(target=windowProcess, args=(action,), kwargs={})
    t.setDaemon(True)
    t.start()

    if isRunning:
        resp = Response(
            {
                "status": "fail",
                "msg" : "other action is in progress"
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    else:
        w = Window()
        w.pubDate = timezone.now()
        w.state = action
        w.save()
        resp = Response(
                {
                    "status": "OK",
                    "msg" : "current action is '%s'" % action
                }
        )

    return resp

"""
@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format = None):
    try:
        snippet = Temperature.objects.get(pk=pk)
    except Temperature.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TemperatureSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TemperatureSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
def snippet_list(request, format = None):
    if request.method == 'GET':
        snippets = Temperature.objects.all()
        serializer = TemperatureSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TemperatureSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""

@api_view(['GET'])
def measure(request):
    sensorOut = Sensor(15, 'DHT22', False)
    sensorOut.readTemp()

    sensorIn = Sensor(14, 'DHT11', False)
    sensorIn.readTemp()

    tIn = Temperature()
    tIn.pubDate = timezone.now()
    tIn.location = "in"
    tIn.temperature = sensorIn.getTemperature()
    tIn.humidity = sensorIn.getHumidity()
    tIn.save()

    tOut = Temperature()
    tOut.pubDate = timezone.now()
    tOut.location = "out"
    tOut.temperature = sensorOut.getTemperature()
    tOut.humidity = sensorOut.getHumidity()
    tOut.save()

    snippets = [tIn, tOut] #Temperature.objects.all()
    serializer = TemperatureSerializer(snippets, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
    #return render(request, 'templates/window/measure.html', {})

# Create your views here.
def index(request):
    return "hiuer die doku"



def windowProcess(action):
    r = Relais(17, 22)
    r.setAction(action)
    r.run()
    return r.isRunning


