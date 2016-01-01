# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import mblogApp.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mblogApp', '0010_auto_20151229_1554'),
    ]

    operations = [
        migrations.CreateModel(
            name='MUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('displayName', models.CharField(max_length=100)),
                ('registerDate', models.DateTimeField()),
                ('location', models.CharField(max_length=100, blank=True)),
                ('description', models.TextField(max_length=254, blank=True)),
                ('webpage', models.URLField(blank=True)),
                ('profileImage', models.ImageField(default=mblogApp.models.randomDefaultImage, upload_to=b'mblogApp/static/media/profile', blank=True)),
                ('following', models.ManyToManyField(related_name='followers', null=True, to='mblogApp.MUser')),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='following',
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(related_name='posts', to='mblogApp.MUser'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='muser',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
