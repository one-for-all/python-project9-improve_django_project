# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-07-14 03:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_auto_20170713_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='created_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='expiration_date',
            field=models.DateField(default=datetime.date(2017, 7, 13)),
            preserve_default=False,
        ),
    ]