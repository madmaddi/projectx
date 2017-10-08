# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-08 09:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0002_auto_20171008_0858'),
    ]

    operations = [
        migrations.RenameField(
            model_name='temperature',
            old_name='temp_value',
            new_name='temperature',
        ),
        migrations.AddField(
            model_name='temperature',
            name='humidity',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
