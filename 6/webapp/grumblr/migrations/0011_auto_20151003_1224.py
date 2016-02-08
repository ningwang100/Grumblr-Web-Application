# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grumblr', '0010_auto_20151003_0824'),
    ]

    operations = [
        migrations.AddField(
            model_name='grumblr',
            name='liker',
            field=models.ManyToManyField(related_name='like', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='follow',
            field=models.ManyToManyField(related_name='followed', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(related_name='newuser', to=settings.AUTH_USER_MODEL),
        ),
    ]
