# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-13 17:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20160210_2122'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='desc',
            field=models.CharField(default='Описание', max_length=200),
            preserve_default=False,
        ),
    ]
