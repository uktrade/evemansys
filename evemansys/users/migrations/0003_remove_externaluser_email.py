# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-05 09:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_employee_externaluser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='externaluser',
            name='email',
        ),
    ]