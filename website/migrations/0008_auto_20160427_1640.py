# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-27 15:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_auto_20160427_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='website/notFound.png', upload_to='website/%Y/%m/%d/'),
        ),
    ]
