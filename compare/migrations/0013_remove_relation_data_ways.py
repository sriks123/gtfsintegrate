# Generated by Django 2.0.6 on 2018-07-27 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compare', '0012_auto_20180726_1906'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='relation_data',
            name='ways',
        ),
    ]
