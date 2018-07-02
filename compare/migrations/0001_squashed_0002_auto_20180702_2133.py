# Generated by Django 2.0.6 on 2018-07-02 22:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('compare', '0001_initial'), ('compare', '0002_auto_20180702_2133')]

    initial = True

    dependencies = [
        ('multigtfs', '0001_squashed_0001_initial'),
        ('osmapp', '0001_squashed_0002_auto_20180627_1205'),
    ]

    operations = [
        migrations.CreateModel(
            name='CMP_Line',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='CMP_Stop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fixed_match', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='by_user', to='osmapp.Node')),
                ('gtfs_stop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='multigtfs.Stop')),
            ],
        ),
        migrations.CreateModel(
            name='itineraries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]