# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-23 12:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_auto_20171223_1622'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='overview',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='task',
            name='rules',
        ),
    ]