# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-22 08:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='finished_date',
            field=models.DateTimeField(null=True),
        ),
    ]
