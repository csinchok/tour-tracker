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
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('src', models.ImageField(upload_to=tourtracker.photos.models.photo_upload_to)),
                ('caption', models.CharField(blank=True, max_length=255, null=True)),
                ('timestamp', models.DateTimeField()),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('ride', models.ForeignKey(blank=True, null=True, to='rides.Ride')),
            ],
        ),
    ]
