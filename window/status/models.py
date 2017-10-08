# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Temperature(models.Model):
    pubDate = models.DateTimeField('date published')
    location = models.CharField(max_length=3)
    temperature = models.FloatField()
    humidity = models.FloatField()


class Window(models.Model):
    pubDate = models.DateTimeField('date published')
    state = models.CharField(max_length=5)