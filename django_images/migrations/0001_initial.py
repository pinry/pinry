# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_images.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(height_field=b'height', width_field=b'width', max_length=255, upload_to=django_images.models.hashed_upload_to)),
                ('height', models.PositiveIntegerField(default=0, editable=False)),
                ('width', models.PositiveIntegerField(default=0, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Thumbnail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(height_field=b'height', width_field=b'width', max_length=255, upload_to=django_images.models.hashed_upload_to)),
                ('size', models.CharField(max_length=100)),
                ('height', models.PositiveIntegerField(default=0, editable=False)),
                ('width', models.PositiveIntegerField(default=0, editable=False)),
                ('original', models.ForeignKey(to='django_images.Image', on_delete=models.CASCADE)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='thumbnail',
            unique_together=set([('original', 'size')]),
        ),
    ]
