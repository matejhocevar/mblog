# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mblogApp', '0002_auto_20151127_1408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='posts',
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(related_name='posts', to='mblogApp.User'),
        ),
    ]
