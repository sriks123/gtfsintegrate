# Generated by Django 2.0.6 on 2018-07-16 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compare', '0007_auto_20180716_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='line_stop',
            name='route_id',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='line_stop',
            name='stop_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='line_stop',
            name='stop_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]