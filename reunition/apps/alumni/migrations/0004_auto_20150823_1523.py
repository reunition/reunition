# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('alumni', '0003_auto_20150813_1842'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ('graduation_last_name',), 'verbose_name_plural': 'People'},
        ),
        migrations.AddField(
            model_name='person',
            name='user',
            field=models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
