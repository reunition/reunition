# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reunions', '0003_auto_20150814_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='reunion',
            name='intro_text',
            field=models.TextField(null=True, blank=True),
        ),
    ]
