# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-07 05:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_result_score'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='result_excel',
            new_name='result_csv',
        ),
    ]
