# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Author'
        db.create_table(u'cbvcrudapp_author', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'cbvcrudapp', ['Author'])

        # Adding model 'Book'
        db.create_table(u'cbvcrudapp_book', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='books', to=orm['cbvcrudapp.Author'])),
        ))
        db.send_create_signal(u'cbvcrudapp', ['Book'])


    def backwards(self, orm):
        # Deleting model 'Author'
        db.delete_table(u'cbvcrudapp_author')

        # Deleting model 'Book'
        db.delete_table(u'cbvcrudapp_book')


    models = {
        u'cbvcrudapp.author': {
            'Meta': {'object_name': 'Author'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'cbvcrudapp.book': {
            'Meta': {'object_name': 'Book'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'books'", 'to': u"orm['cbvcrudapp.Author']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['cbvcrudapp']