# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-05 13:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctionDjango', '0002_auto_20161105_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='deadline',
            field=models.DateTimeField(default=0, verbose_name='deadline'),
        ),
    ]
