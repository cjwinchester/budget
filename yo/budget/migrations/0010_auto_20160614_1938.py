# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-15 00:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0009_income'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='human',
            field=models.CharField(choices=[('laurel', 'Laurel'), ('cody', 'Cody'), ('both', 'Both')], max_length=20),
        ),
        migrations.AlterField(
            model_name='spending',
            name='human',
            field=models.CharField(choices=[('laurel', 'Laurel'), ('cody', 'Cody'), ('both', 'Both')], max_length=20),
        ),
    ]
