# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-08-31 16:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ladder', '0034_auto_20200831_1016'),
    ]

    operations = [
        migrations.CreateModel(
            name='QueueChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('min_mmr', models.PositiveSmallIntegerField(default=0)),
                ('discord_id', models.PositiveIntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='laddersettings',
            name='normal_queue_discord_channel',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='laddersettings',
            name='open_queue_discord_channel',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='laddersettings',
            name='use_queue',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='ladderqueue',
            name='min_mmr',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
