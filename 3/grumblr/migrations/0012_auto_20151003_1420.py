# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0011_auto_20151003_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grumblr',
            name='liker',
            field=models.ManyToManyField(related_name='+', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
