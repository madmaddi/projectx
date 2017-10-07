# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Temperature(models.Model):
    pub_date = models.DateTimeField('date published')
    temp_value = models.CharField(max_length=50)
    temp_type =  models.CharField(max_length=3)

