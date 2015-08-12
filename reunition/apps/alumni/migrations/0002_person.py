# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('graduation_first_name', models.CharField(max_length=100)),
                ('graduation_last_name', models.CharField(max_length=100)),
                ('current_first_name', models.CharField(max_length=100, null=True, blank=True)),
                ('current_last_name', models.CharField(max_length=100, null=True, blank=True)),
                ('graduating_class', models.ForeignKey(to='alumni.GraduatingClass')),
            ],
        ),
    ]
