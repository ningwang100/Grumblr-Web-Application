# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0005_auto_20150920_1830'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='photopath',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='age',
            field=models.CharField(default=b'', max_length=20),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default=b'', upload_to=b'avatar'),
        ),
    ]
