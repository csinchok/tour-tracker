# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('src', models.ImageField(upload_to='')),
                ('caption', models.CharField(null=True, blank=True, max_length=255)),
                ('timestamp', models.DateTimeField()),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('_path', models.TextField()),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('distance', models.FloatField()),
                ('average_speed', models.FloatField()),
                ('ride_time', models.DurationField()),
                ('stopped_time', models.DurationField()),
            ],
        ),
        migrations.AddField(
            model_name='photo',
            name='ride',
            field=models.ForeignKey(null=True, blank=True, to='core.Ride'),
        ),
    ]
