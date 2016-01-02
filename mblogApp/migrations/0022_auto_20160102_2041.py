# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mblogApp.models


class Migration(migrations.Migration):

    dependencies = [
        ('mblogApp', '0021_auto_20160102_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profileImage',
            field=models.ImageField(default=mblogApp.models.randomDefaultImage, upload_to=b'mblogApp/static/media/profile', blank=True),
        ),
    ]
