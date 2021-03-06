# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-16 19:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('runtracker', '0006_auto_20160923_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='run',
            name='calories',
            field=models.FloatField(default=0, verbose_name='Calories'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='dob',
            field=models.DateField(default=datetime.date(1987, 2, 24), verbose_name='Date of birth'),
        ),
    ]
