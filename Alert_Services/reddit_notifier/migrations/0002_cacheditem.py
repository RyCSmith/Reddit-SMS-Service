# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reddit_notifier', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CachedItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subreddit', models.CharField(max_length=200)),
                ('text', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=200)),
                ('last_updated', models.DateTimeField(verbose_name=b'last updated')),
            ],
        ),
    ]
