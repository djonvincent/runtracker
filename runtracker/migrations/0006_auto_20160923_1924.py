# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-23 18:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('runtracker', '0005_auto_20160922_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='dob',
            field=models.DateField(default=datetime.date(1986, 10, 1), verbose_name='Date of birth'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='height',
            field=models.FloatField(default=170.0, verbose_name='Height (cm)'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='mass',
            field=models.FloatField(default=70.0, verbose_name='Weight (kg)'),
        ),
    ]