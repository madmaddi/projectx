# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-08 08:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='temperature',
            old_name='temp_type',
            new_name='location',
        ),
    ]
