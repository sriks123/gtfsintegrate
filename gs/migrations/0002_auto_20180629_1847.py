# Generated by Django 2.0.6 on 2018-06-29 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gtfsform',
            name='feed',
            field=models.IntegerField(blank=True, default=-1),
        ),
    ]