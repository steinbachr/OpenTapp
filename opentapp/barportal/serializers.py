from barportal import enums as e
from barportal.models import Bar, SingleCoupon, GroupCoupon, MobileUser, Menu, MenuItem
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

class SingleCouponSerializer(serializers.ModelSerializer):
    from_date = serializers.DateField(format=e.Formatting.DATE_FORMAT)
    to_date = serializers.DateField(format=e.Formatting.DATE_FORMAT)
    issued_at = serializers.DateTimeField(format=e.Formatting.DATETIME_FORMAT)
    from_time = serializers.TimeField(format=e.Formatting.TIME_FORMAT)
    to_time = serializers.TimeField(format=e.Formatting.TIME_FORMAT)
    
    class Meta:
        model = SingleCoupon
        exclude = ('applies_to',) 
        
   
class GroupCouponSerializer(serializers.ModelSerializer):
    from_date = serializers.DateField(format=e.Formatting.DATE_FORMAT)
    to_date = serializers.DateField(format=e.Formatting.DATE_FORMAT)
    issued_at = serializers.DateTimeField(format=e.Formatting.DATETIME_FORMAT)
    from_time = serializers.TimeField(format=e.Formatting.TIME_FORMAT)
    to_time = serializers.TimeField(format=e.Formatting.TIME_FORMAT)
    
    class Meta:
        model = GroupCoupon
        exclude = ('applies_to',)


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ('price', 'name')   


class MenuSerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(many=True)
    
    class Meta:
        model = Menu
        exclude = ('bar',)
        
        
class BarSerializer(serializers.ModelSerializer):
    group_coupons = GroupCouponSerializer(many=True, source='groupcoupon_set')
    single_coupons = SingleCouponSerializer(many=True, source='singlecoupon_set')    
    menu = MenuSerializer()
    
    class Meta:
        model = Bar
        exclude = ('raw_menu',)        


class MobileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileUser
        fields = ('fb_id', 'name', 'id', 'gcm_id')
