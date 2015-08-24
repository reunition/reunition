# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('alumni', '0004_auto_20150823_1523'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('contacted', models.CharField(blank=True, max_length=10, null=True, choices=[(b'', b'No contact made'), (b'', b'---'), (b'incoming', b'This person contacted the alumni committee'), (b'', b'---'), (b'email', b'Sent email'), (b'facebook', b'Sent Facebook message or request'), (b'phone', b'Made phone call'), (b'text', b'Sent text message'), (b'other', b'Made other contact')])),
                ('text', models.TextField()),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('person', models.ForeignKey(to='alumni.Person')),
            ],
            options={
                'ordering': ('created_by',),
            },
        ),
    ]
