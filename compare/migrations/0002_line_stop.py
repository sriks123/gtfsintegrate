# Generated by Django 2.0.6 on 2018-07-16 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compare', '0001_squashed_0002_auto_20180702_2133'),
    ]

    operations = [
        migrations.CreateModel(
            name='Line_Stop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feed_id', models.IntegerField(blank=True, null=True)),
                ('stop_id', models.IntegerField(blank=True, null=True)),
                ('stop_code', models.CharField(blank=True, max_length=50, null=True)),
                ('stop_name', models.CharField(blank=True, max_length=50, null=True)),
                ('stop_time_stop_seq', models.IntegerField(blank=True, null=True)),
                ('trip_extra_data', models.CharField(blank=True, max_length=100, null=True)),
                ('route_id_db', models.IntegerField(blank=True, null=True)),
                ('route_id', models.CharField(blank=True, max_length=50, null=True)),
                ('route_short_name', models.CharField(blank=True, max_length=50, null=True)),
                ('route_long_name', models.CharField(blank=True, max_length=50, null=True)),
                ('route_desc', models.CharField(blank=True, max_length=50, null=True)),
                ('route_color', models.CharField(blank=True, max_length=50, null=True)),
                ('route_text_color', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]
