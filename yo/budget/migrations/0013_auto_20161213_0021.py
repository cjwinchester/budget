# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-12-13 06:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0012_auto_20161213_0018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='majorexpense',
            name='spending',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='budget.Spending'),
        ),
    ]
