# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-23 08:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_auto_20171220_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='overview',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='rules',
            field=models.TextField(null=True),
        ),
    ]
