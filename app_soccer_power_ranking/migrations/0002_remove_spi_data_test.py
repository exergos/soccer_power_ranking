# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_soccer_power_ranking', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spi_data',
            name='Test',
        ),
    ]
