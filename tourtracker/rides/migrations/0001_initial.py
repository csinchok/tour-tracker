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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
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
    ]
