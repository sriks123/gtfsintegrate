# Generated by Django 2.0.6 on 2018-07-15 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversionapp', '0007_auto_20180715_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='correspondence_route',
            name='color',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='correspondence_route',
            name='text_color',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
