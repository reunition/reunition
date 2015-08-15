# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('alumni', '0003_auto_20150813_1842'),
        ('reunions', '0002_reunion_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rsvp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('attending', models.CharField(blank=True, max_length=1, null=True, choices=[(b'Y', b'Yes'), (b'N', b'No'), (b'M', b'Maybe')])),
                ('current_city', models.CharField(max_length=200, null=True, blank=True)),
                ('contact_method', models.CharField(max_length=5, choices=[(b'email', b'Email'), (b'text', b'Text'), (b'phone', b'Phone Call'), (b'none', b'Please do not send me updates')])),
                ('phone', models.CharField(max_length=50, null=True, blank=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('reunion', models.ForeignKey(to='reunions.Reunion')),
            ],
        ),
        migrations.CreateModel(
            name='RsvpAlumniAttendee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('person', models.ForeignKey(to='alumni.Person')),
                ('rsvp', models.ForeignKey(to='reunions.Rsvp')),
            ],
        ),
        migrations.CreateModel(
            name='RsvpGuestAttendee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100, null=True, blank=True)),
                ('relationship', models.CharField(blank=True, max_length=1, null=True, choices=[(b'P', b'Partner/Spouse'), (b'C', b'Child'), (b'O', b'Other')])),
                ('rsvp', models.ForeignKey(to='reunions.Rsvp')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='rsvpalumniattendee',
            unique_together=set([('rsvp', 'person')]),
        ),
        migrations.AlterUniqueTogether(
            name='rsvp',
            unique_together=set([('created_by', 'reunion')]),
        ),
    ]
