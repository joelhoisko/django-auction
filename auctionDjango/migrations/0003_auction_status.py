# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-07 18:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctionDjango', '0002_auto_20161107_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='status',
            field=models.CharField(choices=[('AC', 'Active'), ('BA', 'Banned'), ('DU', 'Due'), ('AD', 'Adjudicated')], default='AC', max_length=2),
        ),
    ]