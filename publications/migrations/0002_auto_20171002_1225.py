# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-02 12:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='publication',
        ),
        migrations.RemoveField(
            model_name='publication',
            name='contributors',
        ),
        migrations.AddField(
            model_name='publication',
            name='path',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publication',
            name='size',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publication',
            name='type',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publication',
            name='url',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='File',
        ),
    ]
