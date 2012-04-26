# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Pin'
        db.create_table('pins_pin', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.TextField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('image', self.gf('thumbs.ImageWithThumbsField')(max_length=100, sizes=((200, 1000),))),
        ))
        db.send_create_signal('pins', ['Pin'])

        # Adding M2M table for field tags on 'Pin'
        db.create_table('pins_pin_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pin', models.ForeignKey(orm['pins.pin'], null=False)),
            ('tag', models.ForeignKey(orm['pins.tag'], null=False))
        ))
        db.create_unique('pins_pin_tags', ['pin_id', 'tag_id'])

        # Adding model 'Tag'
        db.create_table('pins_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal('pins', ['Tag'])

    def backwards(self, orm):
        # Deleting model 'Pin'
        db.delete_table('pins_pin')

        # Removing M2M table for field tags on 'Pin'
        db.delete_table('pins_pin_tags')

        # Deleting model 'Tag'
        db.delete_table('pins_tag')

    models = {
        'pins.pin': {
            'Meta': {'object_name': 'Pin'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('thumbs.ImageWithThumbsField', [], {'max_length': '100', 'sizes': '((200, 1000),)'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['pins.Tag']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'url': ('django.db.models.fields.TextField', [], {})
        },
        'pins.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['pins']