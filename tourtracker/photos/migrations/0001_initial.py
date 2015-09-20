# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tourtracker.photos.models


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('src', models.ImageField(upload_to=tourtracker.photos.models.photo_upload_to)),
                ('caption', models.CharField(null=True, max_length=255, blank=True)),
                ('timestamp', models.DateTimeField()),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
                ('ride', models.ForeignKey(null=True, related_name='photos', blank=True, to='rides.Ride')),
            ],
        ),
    ]
