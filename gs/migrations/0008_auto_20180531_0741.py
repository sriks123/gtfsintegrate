# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-31 07:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gs', '0007_auto_20180531_0736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gtfsform',
            name='frequency',
            field=models.IntegerField(blank=True, default=3),
        ),
    ]