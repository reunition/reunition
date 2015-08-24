# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reunions', '0006_auto_20150823_1541'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rsvpalumniattendee',
            options={'ordering': ('-rsvp__reunion__year', 'created')},
        ),
    ]
