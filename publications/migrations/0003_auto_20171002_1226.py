# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-02 12:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0002_auto_20171002_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='path',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='publication',
            name='size',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='publication',
            name='type',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='publication',
            name='url',
            field=models.CharField(default='', max_length=255),
        ),
    ]
