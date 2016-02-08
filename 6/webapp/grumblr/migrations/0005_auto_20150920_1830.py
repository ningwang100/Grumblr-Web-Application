# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0004_auto_20150920_1657'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='newuser',
            new_name='user',
        ),
    ]
