# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Thumbnail', fields ['image', 'size']
        db.delete_unique(u'django_images_thumbnail', ['image', 'size'])

        # Adding unique constraint on 'Thumbnail', fields ['original', 'size']
        db.create_unique(u'django_images_thumbnail', ['original_id', 'size'])


    def backwards(self, orm):
        # Removing unique constraint on 'Thumbnail', fields ['original', 'size']
        db.delete_unique(u'django_images_thumbnail', ['original_id', 'size'])

        # Adding unique constraint on 'Thumbnail', fields ['image', 'size']
        db.create_unique(u'django_images_thumbnail', ['image', 'size'])


    models = {
        u'django_images.image': {
            'Meta': {'object_name': 'Image'},
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'django_images.thumbnail': {
            'Meta': {'unique_together': "(('original', 'size'),)", 'object_name': 'Thumbnail'},
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'original': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_images.Image']"}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['django_images']