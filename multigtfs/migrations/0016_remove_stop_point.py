# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-05 14:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('multigtfs', '0015_stop_point'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stop',
            name='point',
        ),
    ]
