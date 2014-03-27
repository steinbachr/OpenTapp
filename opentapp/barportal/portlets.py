from django.template import loader, Context, RequestContext
from django.contrib.auth.models import User
from barwatch.barportal import forms, models
from barwatch.barportal.email import DrinkUpEmail
from barwatch import enums as e 
from barwatch import queries as q
from barwatch import helpers as h
import datetime
import operator
import pdb


class FormProcessor():
    '''a form processor is like a portlet in that it encapsulates business logic, however is different in that
    it isn't at all responsible for display of data, rather it just processes the form it encapsulates'''
    def __init__(self, form, request):
        self.form = form
        self.request = request

    def form_success(self):
        return self.process_form()

    def process_form(self):
        pass


class Portlet(FormProcessor):
    '''Portlet (encapsulate a view)'''
    def __init__(self, tpl_file, request, tab_id='', user=None, form=None):
        FormProcessor.__init__(self, form, request)
        self.tpl_file = tpl_file        
        self.tpl_vars = {}
        self.tab_id = tab_id  
        self.user = user
        
    def render(self):
        self.tpl_vars['tab_id'] = self.tab_id        
                
        template = loader.get_template(self.tpl_file)        
        context = Context(self.tpl_vars)
        return template.render(context) 
      
      
##BAR PORTLETS
class DashboardPortlet(Portlet):
    def __init__(self, request, bar, user):
        Portlet.__init__(self, 'portlets/bar_portlets/dashboard.html', request, tab_id=e.NavigationTabs.DASHBOARD.verbose, user=user)
        self.bar = bar        
        
        all_coups = [(coup, coup.num_redeemed) for coup in q.get_all_coupons(self.bar).single.all()]
        most_redeemed = max(all_coups, key=operator.itemgetter(1)) if all_coups else None        
        
        self.tpl_vars = {'user'          : self.user,
                         'bar'           : self.bar,
                         'most_redeemed' : most_redeemed[0] if most_redeemed else None,
                         'last_five'     : q.get_all_coupons(self.bar).single.order_by('-issued_at').all()[0:5],
                         'active_single_coupons': q.get_active(self.bar).single.all(),
                         'active_group_coupons': q.get_active(self.bar).group.all()}

class BroadcastPortlet(Portlet):
    def __init__(self, request, bar, user):
        Portlet.__init__(self, 'portlets/bar_portlets/broadcast_coupon.html', request, tab_id=e.NavigationTabs.BROADCAST.verbose, user=user)
        self.bar = bar                
        
        self.tpl_vars = {'broadcast_form'        : forms.BroadcastCouponForm(),
                         'single_broadcast_form' : forms.BroadcastSingleCouponForm(),
                         'group_broadcast_form'  : forms.BroadcastGroupCouponForm(),
                         'user'                  : self.user}
        
    def process_form(self):        
        self.form = forms.BroadcastCouponForm(self.request.POST)   
        if self.form.is_valid():            
            deal_type = int(self.form.cleaned_data['deal_type'])            
            
            coupon_from_date = self.form.cleaned_data['coupon_valid_from_date']            
            coupon_to_date = self.form.cleaned_data['coupon_valid_to_date']
            coupon_valid_all_day = self.form.cleaned_data['valid_all_day']            
            coupon_from_time = self.form.cleaned_data['coupon_valid_from_time'] if not coupon_valid_all_day else datetime.time(0, 0, 0) 
            coupon_to_time = self.form.cleaned_data['coupon_valid_to_time'] if not coupon_valid_all_day else datetime.time(23, 59, 59)            
            coupon_issued_datetime = self.bar.get_now
            coupon_one_per_customer = self.form.cleaned_data['one_per_customer']
                        
            if deal_type == e.DealTypes.SINGLE.key:                
                self.form = forms.BroadcastSingleCouponForm(self.request.POST)
                if self.form.is_valid():
                    coupon_desc = self.form.cleaned_data['coupon_description']
                    coupon = models.SingleCoupon(bar=self.bar, coupon_description=coupon_desc, 
                                                 issued_at=coupon_issued_datetime,
                                                 from_date=coupon_from_date, to_date=coupon_to_date, 
                                                 from_time=coupon_from_time, to_time=coupon_to_time,
                                                 one_per_customer=coupon_one_per_customer)                    
            else:
                self.form = forms.BroadcastGroupCouponForm(self.request.POST)
                if self.form.is_valid():
                    tier_one_min = self.form.cleaned_data['tier_one_min']
                    tier_one_max = self.form.cleaned_data['tier_one_max']
                    tier_one_desc = self.form.cleaned_data['tier_one_desc']
                    tier_two_min= self.form.cleaned_data['tier_two_min'] if self.form.cleaned_data['tier_two_min'] != '' else None
                    tier_two_max= self.form.cleaned_data['tier_two_max'] if self.form.cleaned_data['tier_two_max'] != '' else None
                    tier_two_desc = self.form.cleaned_data['tier_two_desc'] if self.form.cleaned_data['tier_two_desc'] != '' else None
                    
                    coupon = models.GroupCoupon(bar=self.bar, coupon_description=tier_one_desc, 
                                                issued_at=coupon_issued_datetime, 
                                                from_date=coupon_from_date, to_date=coupon_to_date, 
                                                from_time=coupon_from_time, to_time=coupon_to_time, 
                                                tier_one_min=tier_one_min, tier_one_max=tier_one_max, 
                                                tier_two_min=tier_two_min, tier_two_max=tier_two_max,
                                                second_tier_description=tier_two_desc, one_per_customer=coupon_one_per_customer)
                                
            coupon.save()

            DrinkUpEmail('coupon_broadcast', 'New coupon broadcast', h.admin_emails(), context={'coupon' : coupon}).send()
            
            return True
                 
        return False                           
            
            
class QueuedCouponsPortlet(Portlet):
    def __init__(self, request, bar, user):
        Portlet.__init__(self, 'portlets/bar_portlets/queued_coupons.html', request, tab_id=e.NavigationTabs.QUEUE.verbose, user=user)
        self.bar = bar
        queued_coups = q.get_queued(self.bar)
        
        self.tpl_vars = {'queued_single_coupons'   : queued_coups.single.all(), 
                         'queued_group_coupons'    : queued_coups.group.all(),
                         'total_issued'            : q.total_published(bar),
                         'total_redeemed'          : q.total_redeemed(bar),
                         'user'                    : self.user}
        
        
class BarProfilePortlet(Portlet):
    def __init__(self, request, bar, user):
        Portlet.__init__(self, 'portlets/bar_portlets/bar_profile.html', request, tab_id=e.NavigationTabs.PROFILE.verbose, user=user)
        self.bar = bar                

        self.tpl_vars = {'edit_bar_form'            : forms.EditBarForm(instance=self.bar),
                         'menu_item_name_name'      : 'drink_name', #these are used as the base names of the dynamically generated form els
                         'menu_item_price_name'     : 'drink_price',
                         'menu_submitted'           :  models.Menu.objects.filter(bar_id=self.bar.id).get() if models.Menu.objects.filter(bar_id=self.bar.id).count() == 1 else None,
                         'bar'                      :  self.bar,
                         'user'                     :  self.user}


class EditProfileProcessor(FormProcessor):
    '''this is a processor because it does not render itself but rather its template file is simply used inside 
    the bar profile template
    '''
    def __init__(self, bar, request):        
        FormProcessor.__init__(self, forms.EditBarForm(instance=bar), request)
        self.bar = bar
                
    def process_form(self):        
        #two different forms, menu and other info
        if self.request.POST.get('item_counter', None) is not None:            
            #menu post
            try:
                bar_menu = models.Menu(bar=self.bar)
                bar_menu.save()
            except Exception:
                bar_menu = self.bar.menu #in this case, the bar already has a menu, so we want to update the existing menu items
        
            input_el_name = 'drink_name' #magic strings coming from the tpl_vars of BarProfilePortlet representing menu input elements
            input_el_price = 'drink_price'
            
            posted_data = self.request.POST
            for i in range(0, int(posted_data.get('item_counter'))):
                drink_name = posted_data.get('%s%d'%(input_el_name,i))
                drink_price = posted_data.get('%s%d'%(input_el_price,i))
                newMenuItem = models.MenuItem(menu=bar_menu, price=drink_price, name=drink_name)
                newMenuItem.save()
            
            return True           
        else:
            self.form = forms.EditBarForm(self.request.POST, self.request.FILES, instance=self.bar)            
            if self.form.is_valid():
                self.form.save()
                return True            
            
            return False



class ViewStatsPortlet(Portlet):
    def __init__(self, request, bar, user):
        Portlet.__init__(self, 'portlets/bar_portlets/view_stats.html', request, tab_id=e.NavigationTabs.STATS.verbose, user=user)
        self.bar = bar        
        self.tpl_vars['bar'] = self.bar

        
class PaymentsPortlet(Portlet):
    def __init__(self, request, bar, user):
        Portlet.__init__(self, 'portlets/bar_portlets/payments.html', request, tab_id=e.NavigationTabs.PAYMENTS.verbose, user=user)
        self.bar = bar
        
        self.tpl_vars = {'num_published': q.total_published_since_last_payment(self.bar),
                         'num_redeemed' : q.coupon_redemptions_since_last_payment(self.bar).count(),
                         'total_owed'   : self.bar.balance,
                         'pay_rate'     : models.Coupon.redemption_rate() * 100,
                         'past_payments': [(index, payment) for index,payment in enumerate(models.Payment.objects.filter(bar_id=self.bar.id).all())],
                         'user'         : self.user}

        
class HelpPortlet(Portlet):
    def __init__(self, request):
        Portlet.__init__(self, 'portlets/bar_portlets/help.html', request, tab_id=e.NavigationTabs.HELP.verbose)                
