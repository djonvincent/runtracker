# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-20 20:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('runtracker', '0003_auto_20160919_1613'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mass', models.FloatField(verbose_name='Weight (kg)')),
                ('height', models.FloatField(verbose_name='Height (cm)')),
                ('age', models.IntegerField(verbose_name='Age')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
