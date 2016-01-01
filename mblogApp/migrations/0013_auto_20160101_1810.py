# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mblogApp', '0012_remove_muser_registerdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='muser',
            name='displayName',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
