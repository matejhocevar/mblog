# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mblogApp', '0011_auto_20160101_1537'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='muser',
            name='registerDate',
        ),
    ]
