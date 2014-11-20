# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coins',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('denominal_coin', models.IntegerField()),
                ('manufacture_date', models.DateField()),
                ('circulation_coin', models.BigIntegerField()),
                ('weight_coin', models.FloatField()),
                ('diametr_coin', models.FloatField()),
                ('thickness_coins', models.FloatField()),
                ('painter', models.CharField(max_length=b'100')),
                ('sculptor', models.CharField(max_length=b'100')),
                ('herd_coin', models.CharField(max_length=b'10000')),
                ('description', models.CharField(max_length=b'1000000')),
                ('item_number', models.CharField(max_length=9)),
                ('photo_obverse', models.ImageField(upload_to=b'')),
                ('photo_reverse', models.ImageField(upload_to=b'')),
                ('link_cbr', models.URLField()),
                ('country', models.ForeignKey(to='coins.Countries')),
            ],
            options={
                'db_table': 'Coins',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CoinToMint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('coin', models.ForeignKey(to='coins.Coins')),
            ],
            options={
                'db_table': 'CoinToMint',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Denominals',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('denominal_name', models.CharField(max_length=b'50')),
                ('country_denominal', models.ForeignKey(to='coins.Countries')),
            ],
            options={
                'db_table': 'Denominals',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Metals',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('metal_description', models.CharField(max_length=b'10000')),
            ],
            options={
                'db_table': 'Metals',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Mints',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mint_name', models.CharField(max_length=b'200')),
                ('mint_abbreviation', models.CharField(max_length=10)),
                ('country', models.ForeignKey(to='coins.Countries')),
            ],
            options={
                'db_table': 'Mints',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='cointomint',
            name='mint',
            field=models.ForeignKey(to='coins.Mints'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coins',
            name='denominal_name',
            field=models.ForeignKey(to='coins.Denominals'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coins',
            name='metal_coin',
            field=models.ForeignKey(to='coins.Metals'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coins',
            name='series',
            field=models.ForeignKey(to='coins.Series'),
            preserve_default=True,
        ),
    ]
