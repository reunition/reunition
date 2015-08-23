# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reunions', '0004_reunion_intro_text'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reunion',
            options={'ordering': ('-year',)},
        ),
        migrations.AlterModelOptions(
            name='rsvp',
            options={'ordering': ('-reunion__year', '-created')},
        ),
        migrations.AlterModelOptions(
            name='rsvpalumniattendee',
            options={'ordering': ('person__graduation_first_name',)},
        ),
        migrations.AlterModelOptions(
            name='rsvpguestattendee',
            options={'ordering': ('first_name',)},
        ),
    ]
