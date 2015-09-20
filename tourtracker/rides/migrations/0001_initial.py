# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('_path', models.TextField()),
                ('map_ratio', models.FloatField()),
                ('ride_file', models.FileField(upload_to='ride_files')),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('distance', models.FloatField()),
                ('average_speed', models.FloatField()),
                ('ride_time', models.DurationField()),
                ('stopped_time', models.DurationField()),
            ],
        ),
    ]
