# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-03 13:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ladder', '0005_auto_20161130_1348'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='matchplayer',
            options={'ordering': ('-match__date', 'team')},
        ),
    ]
