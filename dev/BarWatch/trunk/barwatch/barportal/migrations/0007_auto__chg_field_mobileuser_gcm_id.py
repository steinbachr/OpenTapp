# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'MobileUser.gcm_id'
        db.alter_column('barportal_mobileuser', 'gcm_id', self.gf('django.db.models.fields.TextField')())

    def backwards(self, orm):

        # Changing field 'MobileUser.gcm_id'
        db.alter_column('barportal_mobileuser', 'gcm_id', self.gf('django.db.models.fields.CharField')(max_length=500))

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
        'barportal.bar': {
            'Meta': {'object_name': 'Bar'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'bar_tz': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'cover_photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'hours_from': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'hours_to': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kitchen_hours_from': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'kitchen_hours_to': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '7'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '7'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'raw_menu': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tvs': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'barportal.baruser': {
            'Meta': {'object_name': 'BarUser'},
            'bar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['barportal.Bar']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'barportal.couponredemption': {
            'Meta': {'object_name': 'CouponRedemption'},
            'group_coupon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['barportal.GroupCoupon']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['barportal.MobileUser']", 'null': 'True', 'blank': 'True'}),
            'single_coupon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['barportal.SingleCoupon']", 'null': 'True', 'blank': 'True'}),
            'touch_datetime': ('django.db.models.fields.DateTimeField', [], {})
        },
        'barportal.groupcoupon': {
            'Meta': {'object_name': 'GroupCoupon'},
            'applies_to': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['barportal.MenuItem']", 'null': 'True', 'blank': 'True'}),
            'bar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['barportal.Bar']"}),
            'coupon_description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'from_date': ('django.db.models.fields.DateField', [], {}),
            'from_time': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issued_at': ('django.db.models.fields.DateTimeField', [], {}),
            'num_redeemed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'one_per_customer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'second_tier_description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'tier_one_max': ('django.db.models.fields.IntegerField', [], {}),
            'tier_one_min': ('django.db.models.fields.IntegerField', [], {}),
            'tier_two_max': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tier_two_min': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'to_date': ('django.db.models.fields.DateField', [], {}),
            'to_time': ('django.db.models.fields.TimeField', [], {})
        },
        'barportal.groupmembers': {
            'Meta': {'object_name': 'GroupMembers'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'group_members'", 'to': "orm['barportal.GroupRedemption']"}),
            'has_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['barportal.MobileUser']"})
        },
        'barportal.groupredemption': {
            'Meta': {'object_name': 'GroupRedemption'},
            'applies_to': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['barportal.GroupCoupon']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['barportal.MobileUser']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'barportal.menu': {
            'Meta': {'object_name': 'Menu'},
            'bar': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['barportal.Bar']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'barportal.menuitem': {
            'Meta': {'object_name': 'MenuItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['barportal.Menu']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        },
        'barportal.mobileuser': {
            'Meta': {'object_name': 'MobileUser'},
            'fb_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'gcm_id': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'barportal.payment': {
            'Meta': {'object_name': 'Payment'},
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'bar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['barportal.Bar']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'touch_datetime': ('django.db.models.fields.DateTimeField', [], {})
        },
        'barportal.singlecoupon': {
            'Meta': {'object_name': 'SingleCoupon'},
            'applies_to': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['barportal.MenuItem']", 'null': 'True', 'blank': 'True'}),
            'bar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['barportal.Bar']"}),
            'coupon_description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'from_date': ('django.db.models.fields.DateField', [], {}),
            'from_time': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issued_at': ('django.db.models.fields.DateTimeField', [], {}),
            'num_redeemed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'one_per_customer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'to_date': ('django.db.models.fields.DateField', [], {}),
            'to_time': ('django.db.models.fields.TimeField', [], {})
        },
        'barportal.user': {
            'Meta': {'object_name': 'User'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['barportal']