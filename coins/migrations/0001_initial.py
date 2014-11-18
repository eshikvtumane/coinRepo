# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Countries',
            fields=[
                ('country', models.AutoField(serialize=False, primary_key=True)),
                ('country_name', models.CharField(max_length=200)),
                ('country_flag', models.ImageField(upload_to=b'')),
            ],
            options={
                'db_table': 'Countries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('series', models.AutoField(serialize=False, primary_key=True)),
                ('series_name', models.CharField(max_length=1000)),
                ('country', models.ForeignKey(to='coins.Countries')),
            ],
            options={
                'db_table': 'Series',
            },
            bases=(models.Model,),
        ),
    ]
