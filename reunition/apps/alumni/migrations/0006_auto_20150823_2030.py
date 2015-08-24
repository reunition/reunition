# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0005_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='contacted',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'', b'No contact made'), (b'', b'---'), (b'email', b'Sent email'), (b'fb', b'Sent Facebook message'), (b'phone', b'Made phone call'), (b'text', b'Sent text message'), (b'other', b'Made other contact'), (b'', b'---'), (b'email-in', b'Received email'), (b'fb-in', b'Received Facebook message'), (b'phone-in', b'Received phone call'), (b'text-in', b'Received text message'), (b'other', b'Received other contact')]),
        ),
    ]
