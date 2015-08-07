# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reunion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.PositiveIntegerField()),
                ('starts_on', models.DateField()),
                ('ends_on', models.DateField()),
                ('graduating_class', models.ForeignKey(to='alumni.GraduatingClass')),
            ],
        ),
    ]
