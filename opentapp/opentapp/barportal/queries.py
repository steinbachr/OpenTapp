from django.db.models import F, Q
from opentapp.barportal.models import SingleCoupon as s_coupon
from opentapp.barportal.models import GroupCoupon as g_coupon
from opentapp.barportal.models import CouponRedemption as cr
from opentapp.barportal.models import Payment as payment
import datetime


class StandardCouponQueryResult():
    '''this class will basically just encapsulate the format we want to return the result of coupon queries in'''
    def __init__(self, single_coups, group_coups):
        self.single = single_coups
        self.group = group_coups
        
##STATUS QUERIES##
def get_all_coupons(b):
    '''get all coupons for a bar'''
    all_single = s_coupon.objects.filter(bar__id=b.id)
    all_group = g_coupon.objects.filter(bar__id=b.id)
    
    return StandardCouponQueryResult(all_single, all_group)

def get_active(b):    
    '''get all the active coupons for a bar'''  
    now = b.get_now    
    
    all_single = get_all_coupons(b).single    
    all_group = get_all_coupons(b).group   
                                         
    #filter single coupons (complicated because we're accounting for times in the form 11PM - 1AM => 23:00 - 1:00 => from_time>to_time
    active_single = all_single.filter(Q(Q(from_date__lte=now.date()) & Q(from_time__lte=now.time()) & \
                                      Q(to_date__gte=now.date()) & Q(to_time__gte=now.time())) | \
                                      Q(from_time__gt=F('to_time')) & (Q(from_time__lte=now.time()) | Q(to_time__gte=now.time()))) 

    #filter group coupons
    active_group = all_group.filter(Q(Q(from_date__lte=now.date()) & Q(from_time__lte=now.time()) & \
                                     Q(to_date__gte=now.date()) & Q(to_time__gte=now.time())) | \
                                   Q(from_time__gt=F('to_time')) & (Q(from_time__lte=now.time()) | Q(to_time__gte=now.time())))                              

    return StandardCouponQueryResult(active_single, active_group)

def get_queued(b):
    '''get all the queued coupons for a bar, this includes all coupons that havent expired and have a quantity remaining'''
    now = b.get_now

    all_single = get_all_coupons(b).single
    all_group = get_all_coupons(b).group
    
    #filter coupons
    queued_single = all_single.filter(to_date__gte=now.date())
    queued_group = all_group.filter(to_date__gte=now.date())

    return StandardCouponQueryResult(queued_single, queued_group)
##END STATUS QUERIES##

##COUNT QUERIES##
def total_published(b):
    total_single = get_all_coupons(b).single.all().count()    
    total_group = get_all_coupons(b).group.all().count()
     
    total_single = total_single if total_single and total_single is not None else 0 #cant have None's floating around    
    
    return total_single + total_group

def total_published_since_last_payment(b):
    total_single = coupon_publishes_since_last_payment(b).single.count()
    total_group = coupon_publishes_since_last_payment(b).group.count()

    total_single = total_single if total_single and total_single is not None else 0 #cant have None's floating around    

    return total_single + total_group

def total_redeemed(b):
    total_redeemed = cr.objects.filter(single_coupon__bar__id=b.id).count() + cr.objects.filter(group_coupon__bar__id=b.id).count()
    return total_redeemed
    
def total_active(b):
    pass
def total_active_redeemed(b):
    pass
##END COUNT QUERIES##

##PAYMENT QUERIES##
def my_last_payment(b):
    payments = payment.objects.filter(bar__id=b.id)
    last_payment = payments.order_by('-id')[:1] if payments.count() > 0 else None
    return last_payment

def coupon_redemptions_since_last_payment(b):           
    last_payment = my_last_payment(b)
    last_payment_datetime = last_payment.get().touch_datetime if last_payment else datetime.datetime(2012, 1, 1) #just some date before now
    my_coupon_redemptions = cr.objects.filter(single_coupon__bar__id=b.id)
    
    my_coupon_redemptions = my_coupon_redemptions.filter(touch_datetime__gte=last_payment_datetime) 
    since_last_payment = my_coupon_redemptions.filter(touch_datetime__lte=b.get_now)
        
    return since_last_payment

def coupon_publishes_since_last_payment(b):
    last_payment = my_last_payment(b)
    last_payment_datetime = last_payment.get().touch_datetime if last_payment else datetime.datetime(2012, 1, 1) #just some date before now
    
    my_single_coupon_publishes = get_all_coupons(b).single
    my_group_coupon_publishes = get_all_coupons(b).group

    my_single_coupon_publishes = my_single_coupon_publishes.filter(issued_at__gte=last_payment_datetime).\
                                                            filter(issued_at__lte=b.get_now)
    my_group_coupon_publishes = my_group_coupon_publishes.filter(issued_at__gte=last_payment_datetime).\
                                                          filter(issued_at__lte=b.get_now)    
    
    return StandardCouponQueryResult(my_single_coupon_publishes, my_group_coupon_publishes)
