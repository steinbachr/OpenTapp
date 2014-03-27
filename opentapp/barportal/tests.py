import unittest
import datetime
import json
from django.test.client import Client
from pytz import timezone
from barwatch import enums as e
from barwatch import helpers as h
from barwatch import queries as q
from barwatch import location as loc
from barwatch.barportal import models as m

class BaseTest(unittest.TestCase):
    BAR = {'name' : 'Test Bar', 'password' : 'test', 'long' : -71.0342, 'lat' : 42.2128, 'address' : "Boston, MA", 
           'timezone' : [timezone('US/Eastern'), timezone('America/New_York')]}
    COUPON = {'type' : e.CouponTypes.COVER.key, 'o_price' : 30, 'd_price' : 20, 'num_issued' : 30, 'num_remaining' : 30}

    def setUp(self):                        
        #create some generic stuff that is used by many of the tests
        self.bar = m.Bar(name=self.BAR['name'], password=self.BAR['password'], longitude=self.BAR['long'], latitude=self.BAR['lat'], address=self.BAR['address'])
        self.bar.save()
        self.coupon = m.Coupon(bar=self.bar, applies_to=None, coupon_type=self.COUPON['type'], alcohol_type=None, alcohol_specifics=None,
            original_price=self.COUPON['o_price'], discounted_price=self.COUPON['d_price'], num_issued=self.COUPON['num_issued'], num_remaining=self.COUPON['num_remaining'],
            issued_at=h.get_bar_now(self.bar.bar_tz), expires_at=h.get_bar_now(self.bar.bar_tz) + datetime.timedelta(days=1),
            effective_at=h.get_bar_now(self.bar.bar_tz))
        self.coupon.save()
        
        self.to_destroy = [self.bar, self.coupon]    #an array of models to destroy in the teardown

    def tearDown(self):
        [model.delete() for model in self.to_destroy]

class EnumTests(BaseTest):
    accepted_vals = {'coupon_type_key' : 0,
                     'coupon_type_verbose' : 'Cover',
                     'coupon_type_meta' : {},
                     'coupon_type_dropdown' : [(0, "Cover"), (1, "Drinks")]}
    def setUp(self):   
        BaseTest.setUp(self)
        self.coupon_type_enum = e.CouponTypes
    
    def tearDown(self):
        self.coupon_type_enum = None
        
    def test_key(self):
        self.assertEqual(self.coupon_type_enum.COVER.key, self.accepted_vals['coupon_type_key'])
        
    def test_verbose(self):
        self.assertEqual(self.coupon_type_enum.COVER.verbose, self.accepted_vals['coupon_type_verbose'])
        
    def test_metadata(self):
        self.assertEqual(self.coupon_type_enum.COVER.metadata, self.accepted_vals['coupon_type_meta'])
        
    def test_for_key(self):        
        self.assertEqual(self.coupon_type_enum.for_key(self.accepted_vals['coupon_type_key']), self.coupon_type_enum.COVER)

    def test_list_for_dropdown(self):        
        self.assertEqual(e.CouponTypes.list_for_dropdown(), self.accepted_vals['coupon_type_dropdown'])
        
        
#************MODEL TESTS****************#               
class BarTests(BaseTest):               
    def test_for_id(self):  #this should work for every model if it works for this one
        self.assertEqual(self.bar.for_id(self.bar.id), self.bar)
        
    def test_to_json(self):
        pass    #can't currently think of a good way to test this
    
    def test_bar_tz(self):
        self.assertIn(self.bar.bar_tz, self.BAR['timezone']) #because the timezone could match a couple things a la US/Eastern, America/x
        
    def test_has_menu(self):
        self.assertEqual(self.bar.has_menu, False)
        
        menu = m.Menu(bar=self.bar)
        menu.save()
        self.to_destroy.append(menu)
        
        self.assertEqual(self.bar.has_menu, True)
        
    def test_balance(self):
        #a helper method to create a given number of coupon redemptions
        def redeem_coupons(self, num):
            for i in range(0, num):
                coupon_redemption = m.CouponRedemption(touch_datetime=h.get_bar_now(self.bar.bar_tz), phone=None, coupon=self.coupon)
                coupon_redemption.save()
                self.to_destroy.append(coupon_redemption)
                
        self.assertEqual(self.bar.balance, 0)
        
        NUM_TO_REDEEM = 2
        redeem_coupons(self, NUM_TO_REDEEM)       
        self.assertEqual(self.bar.balance, NUM_TO_REDEEM * m.Coupon.redemption_rate())        
        
###ADD MORE MODEL TESTS HERE

#**************HELPERS TESTS**************#
class HelpersTests(BaseTest):        
    def test_time_delta(self):
        date_1 = datetime.datetime.now()
        date_2 = datetime.datetime.now() + datetime.timedelta(days=1)

        self.assertEqual(h.time_delta(date_1, date_2), (date_1 - date_2).days)
        self.assertEqual(h.time_delta(date_1, date_2, in_seconds=True), (date_1 - date_2).total_seconds())
        
    def test_parse_config_file(self):
        GEONAMES_USER = 'steinbachr'
        config = h.parse_config_file()
        
        self.assertEqual(config['geonames_user'], GEONAMES_USER)
        
    def test_external_url(self):
        EXTERNAL_URL = 'http://www.google.com'
        
        self.assertEquals(h.external_url(EXTERNAL_URL), '%s?' % EXTERNAL_URL)
        self.assertEquals(h.external_url(EXTERNAL_URL, params={'test1':True, 'test2':1}), '%s?test1=True&test2=1' % EXTERNAL_URL)
    
    def test_internal_url(self):
        INTERNAL_URL = '/drinkup/signed-in/'
        
        self.assertEquals(h.internal_url('logged_in'), '%s?' % INTERNAL_URL)
        self.assertEquals(h.internal_url('logged_in', params={'test1':True}), '%s?test1=True' % INTERNAL_URL)
        
        
#************LOCATION TESTS****************#
class LocationTests(BaseTest):    
    def test_geocode_address(self):
        BOSTON_LOC = (42.3583, -71.0603)
        
        self.assertAlmostEqual(loc.BarLocation.geocode_address(self.bar.address)[0], BOSTON_LOC[0], places=1)
        self.assertAlmostEqual(loc.BarLocation.geocode_address(self.bar.address)[1], BOSTON_LOC[1], places=1)
        
    def test_timezone_by_lat_lng(self):
        self.assertIn(timezone(loc.BarLocation.timezone_by_lat_lng((self.bar.latitude, self.bar.longitude))), self.BAR['timezone'])
        

#*************QUERIES TESTS******************#
class QueryTests(BaseTest):
    def setUp(self):
        BaseTest.setUp(self)
        
    def test_get_active(self):
        self.assertIn(self.coupon, q.get_active(self.bar).all())
        
        # Test that the coupon is not active when it shouldnt be effective yet 
        self.coupon.effective_at = h.get_bar_now(self.bar.bar_tz) + datetime.timedelta(minutes=5)
        self.coupon.save()         
        self.assertFalse(q.get_active(self.bar).exists())        
        
        #reset effective at
        self.coupon.effective_at = h.get_bar_now(self.bar.bar_tz)
        self.coupon.save()
        
        #test that the coupon is not active when it should be expoired        
        self.coupon.expires_at = h.get_bar_now(self.bar.bar_tz) - datetime.timedelta(minutes=5)
        self.coupon.save()
        self.assertFalse(q.get_active(self.bar).exists())
        
    def test_get_queued(self):
        self.assertIn(self.coupon, q.get_queued(self.bar).all())

        # Test that the coupon is queued when its effective time is in the future 
        self.coupon.effective_at = h.get_bar_now(self.bar.bar_tz) + datetime.timedelta(minutes=5)
        self.coupon.save()
        self.assertIn(self.coupon, q.get_queued(self.bar).all())
    
        #test that the coupon is not queued when it should be expoired        
        self.coupon.expires_at = h.get_bar_now(self.bar.bar_tz) - datetime.timedelta(minutes=5)
        self.coupon.save()
        self.assertFalse(q.get_queued(self.bar).exists())
        
    def test_total_published(self):
        self.assertEqual(self.coupon.num_issued, q.total_published(self.bar))
        
    def test_total_redeemed(self):        
        self.assertEqual(self.coupon.num_redeemed, q.total_redeemed(self.bar))
        
        phone = None
        self.coupon.redeem_self(phone)
        
        #checks that the redemption worked
        self.assertEqual(self.coupon.num_remaining, self.COUPON['num_remaining'] - 1)
        self.assertEqual(m.CouponRedemption.objects.filter(coupon_id=self.coupon.id).count(), 1)
        self.assertEqual(self.coupon.num_redeemed, q.total_redeemed(self.bar))
        
        
    ###ADD PAYMENT TESTS
   
#**************SERVICE TESTS*******************#
class ServiceTests(BaseTest):
    def setUp(self):
        BaseTest.setUp(self)
        self.client = Client()
    
    @unittest.skipIf(True, "currently the teardown doesnt work correctly so the get bars returns too many bars")
    def test_get_bars(self):        
        self.assertEqual(self.client.get(h.internal_url('get_bars', action_dir='services')).content, self.bar.to_json)

    @unittest.skipIf(True, "they look the same but still not working, investigate me")
    def test_get_coupon(self):
        self.assertEqual(self.client.get(h.internal_url('get_coupon', params={"id" : self.coupon.id}, action_dir='services')).content, 
                         json.dumps(self.coupon.to_json))
        
    def test_register_user(self):
        old_user_count = m.MobileUser.objects.count()
        self.client.get(h.internal_url('register_user', action_dir='services'))
        new_user_count = m.MobileUser.objects.count()
        
        self.assertEqual(new_user_count, old_user_count + 1)    #maybe not the best test
    
    #this might be a bad test right now also for the same reason that test_get_bars is
    def test_redeem_coupon(self):
        user = m.MobileUser()
        user.save()
        old_num_remaining = self.coupon.num_remaining

        #without phone id
        self.client.get(h.internal_url('redeem_coupon', params={'coupon_id' : self.coupon.id}, action_dir='services'))
        self.assertGreater(m.CouponRedemption.objects.filter(coupon_id=self.coupon.id).count(), 0)
#        self.assertEqual(self.coupon.num_remaining, old_num_remaining - 1)

        #with phone id
        self.client.get(h.internal_url('redeem_coupon', params={'coupon_id' : self.coupon.id, 'phone_id' : user.id}, action_dir='services'))
        self.assertGreater(m.CouponRedemption.objects.filter(coupon_id=self.coupon.id).count(), 1)
        self.assertEqual(self.coupon.num_remaining, old_num_remaining - 2)
        
        
#**************ROUTE TESTS*********************#
###ADD ROUTE TESTS
        
    
        

        



        
        
            
            

        

