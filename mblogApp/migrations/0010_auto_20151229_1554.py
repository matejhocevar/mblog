# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mblogApp.models


class Migration(migrations.Migration):

    dependencies = [
        ('mblogApp', '0009_auto_20151229_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profileImage',
            field=models.ImageField(default=mblogApp.models.randomDefaultImage, upload_to=b'mblogApp/static/media/profile', blank=True),
        ),
    ]
