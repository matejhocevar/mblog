# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import mblogApp.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mblogApp', '0014_auto_20160101_1811'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('displayName', models.CharField(max_length=100, blank=True)),
                ('location', models.CharField(max_length=100, blank=True)),
                ('description', models.TextField(max_length=254, blank=True)),
                ('webpage', models.URLField(blank=True)),
                ('profileImage', models.ImageField(default=mblogApp.models.randomDefaultImage, upload_to=b'mblogApp/static/media/profile', blank=True)),
                ('following', models.ManyToManyField(related_name='followers', null=True, to='mblogApp.UserProfile', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='muser',
            name='following',
        ),
        migrations.RemoveField(
            model_name='muser',
            name='user',
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(related_name='posts', to='mblogApp.UserProfile'),
        ),
        migrations.DeleteModel(
            name='MUser',
        ),
    ]
