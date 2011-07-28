# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Concept'
        db.create_table('learn_concept', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='concepts', to=orm['auth.User'])),
        ))
        db.send_create_signal('learn', ['Concept'])

        # Adding model 'Goal'
        db.create_table('learn_goal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('length', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='goals', to=orm['auth.User'])),
        ))
        db.send_create_signal('learn', ['Goal'])

        # Adding model 'Session'
        db.create_table('learn_session', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sessions', to=orm['auth.User'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('length', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('learn', ['Session'])

        # Adding model 'UserProfile'
        db.create_table('learn_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('emailRemind', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('textRemind', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('phoneRemind', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('timeOfRemind', self.gf('django.db.models.fields.TimeField')(null=True)),
            ('monMin', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('tueMin', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('wedMin', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('thuMin', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('friMin', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('satMin', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('sunMin', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('learn', ['UserProfile'])


    def backwards(self, orm):
        
        # Deleting model 'Concept'
        db.delete_table('learn_concept')

        # Deleting model 'Goal'
        db.delete_table('learn_goal')

        # Deleting model 'Session'
        db.delete_table('learn_session')

        # Deleting model 'UserProfile'
        db.delete_table('learn_userprofile')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'learn.concept': {
            'Meta': {'object_name': 'Concept'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'concepts'", 'to': "orm['auth.User']"})
        },
        'learn.goal': {
            'Meta': {'object_name': 'Goal'},
            'day': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'goals'", 'to': "orm['auth.User']"})
        },
        'learn.session': {
            'Meta': {'object_name': 'Session'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sessions'", 'to': "orm['auth.User']"})
        },
        'learn.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'emailRemind': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'friMin': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monMin': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'phoneRemind': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'satMin': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sunMin': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'textRemind': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thuMin': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'timeOfRemind': ('django.db.models.fields.TimeField', [], {'null': 'True'}),
            'tueMin': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'wedMin': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['learn']
