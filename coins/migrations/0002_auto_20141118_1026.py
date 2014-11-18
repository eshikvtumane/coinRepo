# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='series_name',
            field=models.CharField(max_length=100000),
            preserve_default=True,
        ),
    ]
