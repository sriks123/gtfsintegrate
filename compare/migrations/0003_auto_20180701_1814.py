# Generated by Django 2.0.6 on 2018-07-01 18:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('multigtfs', '0001_squashed_0001_initial'),
        ('osmapp', '0001_squashed_0002_auto_20180627_1205'),
        ('compare', '0002_auto_20180701_1813'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OSM_Node_CMP',
            new_name='CMP_Stop',
        ),
    ]
