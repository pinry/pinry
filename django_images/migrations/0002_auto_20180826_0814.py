# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import core.utils


class Migration(migrations.Migration):

    dependencies = [
        ('django_images', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to=core.utils.upload_path, width_field='width', max_length=255, height_field='height'),
        ),
        migrations.AlterField(
            model_name='thumbnail',
            name='image',
            field=models.ImageField(upload_to=core.utils.upload_path, width_field='width', max_length=255, height_field='height'),
        ),
    ]
