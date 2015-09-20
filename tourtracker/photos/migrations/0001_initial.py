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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('src', models.ImageField(upload_to=tourtracker.photos.models.photo_upload_to)),
                ('caption', models.CharField(null=True, max_length=255, blank=True)),
                ('timestamp', models.DateTimeField()),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
                ('ride', models.ForeignKey(to='rides.Ride', blank=True, related_name='photos', null=True)),
            ],
        ),
    ]
