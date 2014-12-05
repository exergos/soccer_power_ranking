# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='elo_data',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('Team', models.CharField(max_length=30)),
                ('ELO', models.DecimalField(decimal_places=2, max_digits=65)),
                ('finish_1', models.DecimalField(decimal_places=30, max_digits=65)),
                ('finish_2', models.DecimalField(decimal_places=30, max_digits=65)),
                ('finish_3', models.DecimalField(decimal_places=30, max_digits=65)),
                ('finish_4', models.DecimalField(decimal_places=30, max_digits=65)),
                ('finish_5', models.DecimalField(decimal_places=30, max_digits=65)),
                ('finish_6', models.DecimalField(decimal_places=30, max_digits=65)),
                ('finish_7', models.DecimalField(decimal_places=30, max_digits=65)),
                ('finish_8', models.DecimalField(decimal_places=30, max_digits=65)),
                ('finish_9', models.DecimalField(decimal_places=30, max_digits=65)),
                ('finish_10', models.DecimalField(decimal_places=30, max_digits=65)),
                ('finish_11', models.DecimalField(decimal_places=30, max_digits=65)),
                ('finish_12', models.DecimalField(decimal_places=30, max_digits=65)),
                ('finish_13', models.DecimalField(decimal_places=30, max_digits=65)),
                ('finish_14', models.DecimalField(decimal_places=30, max_digits=65)),
                ('finish_15', models.DecimalField(decimal_places=30, max_digits=65)),
                ('finish_16', models.DecimalField(decimal_places=30, max_digits=65)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='spi_data',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('Team', models.CharField(max_length=30)),
                ('Test', models.CharField(max_length=30)),
                ('SPI', models.DecimalField(decimal_places=2, max_digits=65)),
                ('off_rating', models.DecimalField(decimal_places=2, max_digits=65)),
                ('def_rating', models.DecimalField(decimal_places=2, max_digits=65)),
                ('finish_1', models.DecimalField(decimal_places=30, max_digits=65)),
                ('finish_2', models.DecimalField(decimal_places=30, max_digits=65)),
                ('finish_3', models.DecimalField(decimal_places=30, max_digits=65)),
                ('finish_4', models.DecimalField(decimal_places=30, max_digits=65)),
                ('finish_5', models.DecimalField(decimal_places=30, max_digits=65)),
                ('finish_6', models.DecimalField(decimal_places=30, max_digits=65)),
                ('finish_7', models.DecimalField(decimal_places=30, max_digits=65)),
                ('finish_8', models.DecimalField(decimal_places=30, max_digits=65)),
                ('finish_9', models.DecimalField(decimal_places=30, max_digits=65)),
                ('finish_10', models.DecimalField(decimal_places=30, max_digits=65)),
                ('finish_11', models.DecimalField(decimal_places=30, max_digits=65)),
                ('finish_12', models.DecimalField(decimal_places=30, max_digits=65)),
                ('finish_13', models.DecimalField(decimal_places=30, max_digits=65)),
                ('finish_14', models.DecimalField(decimal_places=30, max_digits=65)),
                ('finish_15', models.DecimalField(decimal_places=30, max_digits=65)),
                ('finish_16', models.DecimalField(decimal_places=30, max_digits=65)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
