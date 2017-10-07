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

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

from .serializer import TemperatureSerializer

FILEPATH = "/home/pi/"

@api_view(['GET'])
def windowState(request):
    # windowState
    windowState = "unknown"
    f = open("%s./windowStatus" % FILEPATH, "r")
    if f:
        windowState = f.readline()
        f.close()

    return Response({'state': windowState})

@api_view(['GET'])
def tempList(request, key = None, format = None):
    # if request.query_params.get('key') != None:
    print request.query_params
    if request.method == 'GET':
        location = request.query_params.get('location')
        if location != None:
            snippets = Temperature.objects.filter(temp_type=location).order_by('-pub_date')
        else:
            snippets = Temperature.objects.order_by('-pub_date')

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
        print snippet
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
            }
        )
    else:
        resp = Response(
                {
                    "status": "OK",
                    "msg" : "current action is '%s'" % action
                }
        )

    return resp


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format = None):
    try:
        snippet = Temperature.objects.get(pk=pk)
    except Temperature.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        #return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TemperatureSerializer(snippet)
        return Response(serializer.data)
        #return JsonResponse(serializer.data)

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
            #return JsonResponse(serializer.data, status=201)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #return JsonResponse(serializer.errors, status=400)


# Create your views here.
def index(request):
    return ""
    #return status(request, "", "")


def windowProcess(action):
    r = Relais(17, 22)
    r.setAction(action)
    r.run()
    return r.isRunning

def measure(request):
    sensorOut = Sensor(15, 'DHT22', False)
    sensorOut.readTemp()
    
    sensorIn = Sensor(14, 'DHT11', False)
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
    


