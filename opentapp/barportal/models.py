from django.db import models
from django.contrib.auth.models import User
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
import helpers as h
import enums as e
import datetime
from pytz import timezone

class Bar(models.Model):
    name = models.CharField(max_length=200)  
    #files
    cover_photo = models.ImageField(upload_to='bar_photos/', blank=True, null=True)
    raw_menu = models.FileField(upload_to='bar_menus/', blank=True, null=True)
    #location
    longitude = models.DecimalField(max_digits=10, decimal_places=7)    
    latitude = models.DecimalField(max_digits=10, decimal_places=7)   
    address = models.CharField(max_length=200)     
    #time info
    hours_from = models.TimeField(blank=True, null=True) 
    hours_to = models.TimeField(blank=True, null=True)
    kitchen_hours_from = models.TimeField(blank=True, null=True)
    kitchen_hours_to = models.TimeField(blank=True, null=True)
    bar_tz = models.CharField(max_length=100)
    #meta info
    phone = models.CharField(max_length=15, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)        
    tvs = models.BooleanField()
    rating = models.IntegerField(blank=True, null=True)

    @classmethod
    def for_id(cls, id):
        '''a method to select the bar that has the supplied login credentials'''
        result = cls.objects.get(pk=id)
        return result        
    
    @property 
    def bar_tz_info(self):
        return timezone(self.bar_tz)
    
    @property
    def get_now(self):
        return datetime.datetime.now(tz=self.bar_tz_info)
    
    @property
    def has_menu(self):
        return Menu.objects.filter(bar=self).count() == 1       
    
    @property
    def balance(self):
        from barportal import queries as q

        redemptions_since_last_payment = q.coupon_redemptions_since_last_payment(self).count() * Coupon.redemption_rate()
        return redemptions_since_last_payment    

class BarUser(models.Model):
    user = models.OneToOneField(User)
    bar = models.ForeignKey(Bar)

    @classmethod
    def for_u_id(cls, id):
        '''a method to select the bar that has the supplied login credentials'''
        result = cls.objects.get(user__id=id)
        return result
    
    @classmethod
    def for_bar_id(cls, id):
        '''a method to select the bar that has the supplied login credentials'''
        result = cls.objects.get(bar__id=id)
        return result

class Menu(models.Model):
    bar = models.OneToOneField(Bar)   
    
    @property
    def menu_items(self):
        return MenuItem.objects.filter(menu=self).all()     
    

class MenuItem(models.Model):
    menu = models.ForeignKey(Menu)    
    price = models.DecimalField(max_digits=5, decimal_places=2)
    name = models.CharField(max_length=200)

    @classmethod
    def for_id(cls, id):
        '''a method to select the bar that has the supplied login credentials'''
        result = cls.objects.get(pk=id)
        return result
    

class Coupon(models.Model):
    bar = models.ForeignKey(Bar)
    applies_to = models.ForeignKey(MenuItem, blank=True, null=True) #not used yet        
    coupon_description = models.CharField(max_length=200) 
    #date fields
    issued_at = models.DateTimeField()
    from_date = models.DateField()
    to_date = models.DateField()
    from_time = models.TimeField()
    to_time = models.TimeField()
    #quantity fields
    num_redeemed = models.IntegerField(default=0)
    #boolean fields
    one_per_customer = models.BooleanField()

    class Meta:
        abstract = True
                                 
    @classmethod
    def redemption_rate(cls):
        return .15   

    @property
    def is_active(self):
        '''although we have a query method to get a list of all active coupons and we can use this 
        to determine whether this coupon is active by seeing if its in the list, that is expensive because
        for each coupon we're checking, the time required is O(n), so if we wanted to check n coupons, would take O(n^2) time'''
        now = self.bar.get_now
        within_date = self.from_date <= now.date() and self.to_date >= now.date()        
        goes_over_midnight = self.from_time > self.to_time #weird stuff happens when the valid times are in the form 11PM-1AM          
        
        if within_date:
            if goes_over_midnight:
                return now.time() >= self.from_time and now.time() <= datetime.time(23, 59) or \
                       now.time() <= self.to_time and now.time() >= datetime.time(0, 0)
            else:                
                return self.from_time <= now.time() and self.to_time >= now.time()


class SingleCoupon(Coupon):    
    @classmethod
    def for_id(cls, id):
        result = cls.objects.get(pk=id)
        return result

    @property
    def type(self):
        return e.DealTypes.SINGLE

    def redeem_self(self, phone):
        if not Coupon.is_active:
            return False
        
        redemption = CouponRedemption(touch_datetime=self.bar.get_now, phone=phone, single_coupon=self)
        redemption.save()

        self.num_redeemed += 1
        self.save()

        return True


class GroupCoupon(Coupon):    
    tier_one_min = models.IntegerField()
    tier_one_max = models.IntegerField()    
    tier_two_min = models.IntegerField(blank=True, null=True)
    tier_two_max = models.IntegerField(blank=True, null=True)  
    second_tier_description = models.CharField(max_length=200, blank=True, null=True)

    @classmethod
    def for_id(cls, id):
        result = cls.objects.get(pk=id)
        return result
    
    @property
    def type(self):
        return e.DealTypes.GROUP

    def group_invite(self, user, group):
        '''
            create the pending redemption which will track information about the group 
            the specified user wants to redeem with. Also responsible for push notifications
        '''
        pending_redemption = GroupRedemption(creator=user, applies_to=self)
        pending_redemption.save()
        member_ids = []

        for member in group:
            member_if_exists = MobileUser.objects.filter(fb_id=member).all()
            if len(member_if_exists) > 0:
                mem = member_if_exists[0]
                gm = GroupMembers(group=pending_redemption, user=mem)
                gm.save()
                #add mobile user id to list of ids we will send gcm message to
                member_ids.append(mem.gcm_id)
        
        h.send_gcm_message(member_ids, {'coupon_id' : self.id, 'group_id' : pending_redemption.id})
                
        
    def redeem_self(self, user):
        if not Coupon.is_active:
            return False  
        
        gr = GroupRedemption.objects.filter(creator=user).filter(applies_to=self).get()
        return gr.perform_redemption
   

class MobileUser(models.Model):    
    gcm_id = models.TextField()
    fb_id = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)    

    @classmethod
    def for_id(cls, id):
        '''a method to select the bar that has the supplied login credentials'''
        result = cls.objects.get(pk=id)
        return result


class GroupRedemption(models.Model):
    creator = models.ForeignKey(MobileUser)
    applies_to = models.ForeignKey(GroupCoupon)
    
    @property
    def perform_redemption(self):
        confirmed_count = self.group_members.filter(has_confirmed=True).count()         
        return_val = None
        
        if (confirmed_count < self.applies_to.tier_one_min):
            #doesnt make the first tier
            return_val = e.PossibleGroupRedemptionResults.FAIL
        elif (confirmed_count >= self.applies_to.tier_one_min and (self.applies_to.tier_two_min is None or \
                                                                   confirmed_count < self.applies_to.tier_two_min)):
            self.applies_to.num_redeemed += 1
            return_val = e.PossibleGroupRedemptionResults.TIER_ONE
        else:
            self.applies_to.num_redeemed += 1
            return_val = e.PossibleGroupRedemptionResults.TIER_TWO
            
        self.applies_to.save()
        
        return return_val
    
    
class GroupMembers(models.Model):
    group = models.ForeignKey(GroupRedemption, related_name="group_members")
    user = models.ForeignKey(MobileUser)
    has_confirmed = models.BooleanField(default=False)


class CouponRedemption(models.Model):
    '''a coupon redemption, that is when a user redeems an instance of a coupon'''
    touch_datetime = models.DateTimeField()
    phone = models.ForeignKey(MobileUser, blank=True, null=True) #can be blank because perhaps we were unable to get users phone_id for some reason, should still allow them to redeem coupons
    single_coupon = models.ForeignKey(SingleCoupon, blank=True, null=True)    
    group_coupon = models.ForeignKey(GroupCoupon, blank=True, null=True)       
    
    def save(self, *args, **kwargs):
        self.touch_datetime = h.get_now()
        
        super(CouponRedemption, self).save(*args, **kwargs)
        
class Payment(models.Model):
    '''a Payment by a bar'''
    touch_datetime = models.DateTimeField()
    bar = models.ForeignKey(Bar)
    amount = models.IntegerField()

