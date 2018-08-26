# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Image'
        db.create_table(u'django_images_image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=255)),
            ('height', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('width', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'django_images', ['Image'])

        # Adding model 'Thumbnail'
        db.create_table(u'django_images_thumbnail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_images.Image'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=255)),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('height', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('width', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'django_images', ['Thumbnail'])

        # Adding unique constraint on 'Thumbnail', fields ['image', 'size']
        db.create_unique(u'django_images_thumbnail', ['image', 'size'])


    def backwards(self, orm):
        # Removing unique constraint on 'Thumbnail', fields ['image', 'size']
        db.delete_unique(u'django_images_thumbnail', ['image', 'size'])

        # Deleting model 'Image'
        db.delete_table(u'django_images_image')

        # Deleting model 'Thumbnail'
        db.delete_table(u'django_images_thumbnail')


    models = {
        u'django_images.image': {
            'Meta': {'object_name': 'Image'},
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'django_images.thumbnail': {
            'Meta': {'unique_together': "(('image', 'size'),)", 'object_name': 'Thumbnail'},
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'original': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_images.Image']"}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['django_images']