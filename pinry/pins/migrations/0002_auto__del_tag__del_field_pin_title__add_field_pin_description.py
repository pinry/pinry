# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table('pins_tag')

        # Deleting field 'Pin.title'
        db.delete_column('pins_pin', 'title')

        # Adding field 'Pin.description'
        db.add_column('pins_pin', 'description',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Removing M2M table for field tags on 'Pin'
        db.delete_table('pins_pin_tags')

    def backwards(self, orm):
        # Adding model 'Tag'
        db.create_table('pins_tag', (
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=70)),
        ))
        db.send_create_signal('pins', ['Tag'])


        # User chose to not deal with backwards NULL issues for 'Pin.title'
        raise RuntimeError("Cannot reverse this migration. 'Pin.title' and its values cannot be restored.")
        # Deleting field 'Pin.description'
        db.delete_column('pins_pin', 'description')

        # Adding M2M table for field tags on 'Pin'
        db.create_table('pins_pin_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pin', models.ForeignKey(orm['pins.pin'], null=False)),
            ('tag', models.ForeignKey(orm['pins.tag'], null=False))
        ))
        db.create_unique('pins_pin_tags', ['pin_id', 'tag_id'])

    models = {
        'pins.pin': {
            'Meta': {'object_name': 'Pin'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('thumbs.ImageWithThumbsField', [], {'max_length': '100', 'sizes': '((200, 1000),)'}),
            'url': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['pins']