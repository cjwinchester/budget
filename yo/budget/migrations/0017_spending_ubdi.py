# Generated by Django 2.0.1 on 2018-04-18 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0016_budget_complete'),
    ]

    operations = [
        migrations.AddField(
            model_name='spending',
            name='ubdi',
            field=models.BooleanField(default=False, verbose_name='Unanticipated big-dollar item'),
        ),
    ]