# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-10 04:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0015_auto_20170109_0309'),
    ]

    operations = [
        migrations.AddField(
            model_name='budget',
            name='complete',
            field=models.BooleanField(default=False),
        ),
    ]
