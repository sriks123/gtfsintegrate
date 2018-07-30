# Generated by Django 2.0.6 on 2018-07-29 04:22

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compare', '0015_auto_20180727_1155'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='relation_data',
            name='nodes',
        ),
        migrations.RemoveField(
            model_name='relation_data',
            name='relations',
        ),
        migrations.AddField(
            model_name='relation_data',
            name='relation_ids',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='relation_data',
            name='relation_info',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=200, null=True), size=None), blank=True, null=True, size=None),
        ),
    ]
