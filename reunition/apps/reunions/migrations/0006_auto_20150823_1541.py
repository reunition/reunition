# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reunions', '0005_auto_20150823_1523'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rsvpalumniattendee',
            options={'ordering': ('-rsvp__reunion__year', 'person__graduation_first_name')},
        ),
        migrations.AlterModelOptions(
            name='rsvpguestattendee',
            options={'ordering': ('-relationship', 'first_name')},
        ),
    ]
