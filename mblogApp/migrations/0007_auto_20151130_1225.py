# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mblogApp', '0006_auto_20151130_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to=b'mblogApp/media/img/post', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='profileImage',
            field=models.ImageField(upload_to=b'mblogApp/media/img/profile', blank=True),
        ),
    ]
