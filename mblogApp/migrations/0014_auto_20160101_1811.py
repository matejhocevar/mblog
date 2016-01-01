# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mblogApp', '0013_auto_20160101_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='muser',
            name='following',
            field=models.ManyToManyField(related_name='followers', null=True, to='mblogApp.MUser', blank=True),
        ),
    ]
