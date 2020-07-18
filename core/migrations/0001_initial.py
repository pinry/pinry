# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('users', '__first__'),
        ('django_images', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(null=True)),
                ('origin', models.URLField(null=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('published', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('django_images.image',),
        ),
        migrations.AddField(
            model_name='pin',
            name='image',
            field=models.ForeignKey(related_name='pin', to='core.Image', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='pin',
            name='submitter',
            field=models.ForeignKey(to='users.User', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='pin',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
    ]
