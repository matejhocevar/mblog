# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mblogApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(related_name='follower', null=True, to='mblogApp.User'),
        ),
        migrations.AlterField(
            model_name='user',
            name='posts',
            field=models.ForeignKey(to='mblogApp.Post', null=True),
        ),
    ]
