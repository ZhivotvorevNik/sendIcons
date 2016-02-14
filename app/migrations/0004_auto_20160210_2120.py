# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-10 21:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_zone_votes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='pub_date',
        ),
        migrations.RemoveField(
            model_name='service',
            name='zone',
        ),
        migrations.AddField(
            model_name='service',
            name='zones',
            field=models.ManyToManyField(to='app.Zone'),
        ),
    ]