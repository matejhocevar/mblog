# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mblogApp', '0004_auto_20151127_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to=b'', blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='profileImage',
            field=models.ImageField(upload_to=b'', blank=True),
        ),
    ]
