# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-27 22:31
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osmapp', '0002_auto_20180519_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='way',
            name='geom',
            field=django.contrib.gis.db.models.fields.LineStringField(blank=True, null=True, srid=4326),
        ),
        migrations.AlterField(
            model_name='node',
            name='visible',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='osm_relation',
            name='visible',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='way',
            name='visible',
            field=models.BooleanField(),
        ),
    ]