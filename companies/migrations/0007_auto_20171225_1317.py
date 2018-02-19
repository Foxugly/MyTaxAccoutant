# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-12-25 12:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0006_auto_20171224_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Name of the company'),
        ),
        migrations.AlterField(
            model_name='modeltrimester',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Name of the model trimester'),
        ),
    ]
