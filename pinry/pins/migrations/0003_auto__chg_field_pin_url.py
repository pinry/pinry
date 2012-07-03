# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Pin.url'
        db.alter_column('pins_pin', 'url', self.gf('django.db.models.fields.TextField')(null=True))
    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Pin.url'
        raise RuntimeError("Cannot reverse this migration. 'Pin.url' and its values cannot be restored.")
    models = {
        'pins.pin': {
            'Meta': {'ordering': "['-id']", 'object_name': 'Pin'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('thumbs.ImageWithThumbsField', [], {'max_length': '100', 'sizes': '((200, 1000),)'}),
            'url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['pins']