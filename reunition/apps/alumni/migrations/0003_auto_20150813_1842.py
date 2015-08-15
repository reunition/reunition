# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0002_person'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='graduatingclass',
            options={'verbose_name_plural': 'Graduating Classes'},
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name_plural': 'People'},
        ),
        migrations.AddField(
            model_name='person',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='verified',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
