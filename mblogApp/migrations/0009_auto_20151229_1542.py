# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mblogApp.models


class Migration(migrations.Migration):

    dependencies = [
        ('mblogApp', '0008_auto_20151130_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profileImage',
            field=models.ImageField(default=mblogApp.models.randomDefaultImage, upload_to=b'mblogApp/static/media/img/profile', blank=True),
        ),
    ]
