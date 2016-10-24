# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-24 16:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20160423_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='downvoteList',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='upvoteList',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='was_downvoted',
            field=models.IntegerField(default=0, null=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='was_upvoted',
            field=models.IntegerField(default=0, null=0),
            preserve_default=False,
        ),
    ]
