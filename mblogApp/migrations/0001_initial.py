# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('postTime', models.DateTimeField()),
                ('locationTown', models.CharField(max_length=100, blank=True)),
                ('locationCountry', models.CharField(max_length=100, blank=True)),
                ('content', models.TextField(max_length=800)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=50)),
                ('displayName', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('registerDate', models.DateTimeField()),
                ('location', models.CharField(max_length=100, blank=True)),
                ('description', models.TextField(max_length=254, blank=True)),
                ('webpage', models.URLField(blank=True)),
                ('following', models.ManyToManyField(related_name='follower', to='mblogApp.User')),
                ('posts', models.ForeignKey(to='mblogApp.Post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(to='mblogApp.User'),
        ),
    ]
