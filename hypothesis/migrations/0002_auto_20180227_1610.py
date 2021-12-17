# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-02-27 16:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hypothesis', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hypothesis',
            name='token',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='hypothesis',
            name='api',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='hypothesis',
            name='delta',
            field=models.IntegerField(default=15),
        ),
    ]
