from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render
from opentapp.barportal import forms, models
from opentapp.barportal.portlets import *
from opentapp.barportal.serializers import *
import opentapp.barportal.helpers as h
from opentapp.barportal.email import DrinkUpEmail
from django.contrib.auth import authenticate, login
from location import BarLocation as bar_loc
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

##HOME ACTIONS
#this is terrible, TODO: refactor
def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('barwatch.opentapp.barportal.views.logged_in', args=(request.user.id,)))
            
    login_hidden = True
    signup_hidden = True
    signup_success = request.GET.get('signup_success', False)

    login_form = forms.LoginForm()
    signup_form = forms.BarSignupForm({'form_name' : 'signup_form'})        
        
    if request.method == 'POST':
        form_name = request.POST.get('form_name', None)        
        #signup submission        
        if form_name == 'signup_form':            
            signup_form = forms.BarSignupForm(request.POST, request.FILES)            
            if signup_form.is_valid():    
                new_bar = signup_form.save(commit=False)
                username = signup_form.cleaned_data['username']
                password = signup_form.cleaned_data['password']
                email = signup_form.cleaned_data['email']             
    
                (lat, lng) = bar_loc.geocode_address(new_bar.address)
                bar_tz = bar_loc.timezone_by_lat_lng((lat, lng))
                
                new_bar.bar_tz = bar_tz
                new_bar.latitude = str(lat)
                new_bar.longitude = str(lng)
                new_bar.save()
    
                new_user = User.objects.create_user(username, email=email, password=password)
                new_user.save()
                bar_user = models.BarUser(user=new_user, bar=new_bar)
                bar_user.save()
    
                mail_all = [DrinkUpEmail('registration_received', 'Thanks for signing up, we\'ve got your request', [new_user.email])]
                mail_all.append(DrinkUpEmail('registration_received_admin', 'Bar request pending', h.admin_emails(),
                    context={'email':new_user.email, 
                             'bar_name':new_bar.name, 
                             'bar_phone':new_bar.phone, 
                             'username':new_user.username, 
                             'menu_submitted':new_bar.raw_menu is not None}))
    
                for mailer in mail_all:
                    mailer.send()
    
                return HttpResponseRedirect(h.url(reverse('opentapp.barportal.views.home'), {'signup_success' : True}))
            else:
                signup_hidden = False
        else:            
            #login submission
            login_form = forms.LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
    
                user = authenticate(username=username, password=password) 
                login(request, user)
                request.session['user_id'] = request.user.id #we need to hold the original user in the session to make sure they dont try to switch users during the session
    
                return HttpResponseRedirect(reverse('opentapp.barportal.views.logged_in', args=(request.user.id,)))
            else:            
                login_hidden = False         
                
    tpl_vars = {'login_form'       : login_form,
                'login_hidden'     : login_hidden,
                'signup_form'      : signup_form,                
                'signup_hidden'    : signup_hidden,
                'signup_success'   : signup_success,
                'app_name'         : h.parse_config_file().get('app_name')} 
    
    context = RequestContext(request, tpl_vars)    
    return render_to_response('pages/frontpage.html', context)


##BAR ACTIONS
@login_required
def logged_in(request, user=0):
    user = int(user)

    #if the use tries to switch to another user during his session, log him out
    if request.session['user_id'] != user:
        return logout_user(request)
            
    b_user = models.BarUser.for_u_id(user)
    user = b_user.user
    bar = b_user.bar        
       
    broadcast_success = request.GET.get('broadcast_popup_success', None)    
    if broadcast_success is not None:        
        broadcast_success = (int(broadcast_success) == 1)
    
    dashboard_portlet = DashboardPortlet(request, bar, user)    
    broadcast_portlet = BroadcastPortlet(request, bar, user)
    queued_portlet = QueuedCouponsPortlet(request, bar, user)
    profile_portlet = BarProfilePortlet(request, bar, user)        
    stats_portlet = ViewStatsPortlet(request, bar, user)
    payments_portlet = PaymentsPortlet(request, bar, user)
    help_portlet = HelpPortlet(request)
        
    tpl_vars = {'app_name'          : h.parse_config_file().get('app_name'),
                'bar'               : bar,                
                'nav_tabs'          : e.NavigationTabs,
                'selected_tab'      : request.GET.get('selected_tab', e.NavigationTabs.DASHBOARD.verbose),
                'portlets'          : [dashboard_portlet, broadcast_portlet, queued_portlet, profile_portlet, stats_portlet, payments_portlet, help_portlet],
                'broadcast_hidden'  : broadcast_success is None,
                'broadcast_success' : broadcast_success}
    
    context = RequestContext(request, tpl_vars)
    return render_to_response('pages/logged_in.html', context)

def logout_user(request):
    logout(request)    
    return HttpResponseRedirect(reverse('opentapp.barportal.views.home'))

@login_required
def broadcast_coupon(request, user=0):
    b_user = models.BarUser.for_u_id(user)
    user = b_user.user
    bar = b_user.bar
    broadcast_portlet = BroadcastPortlet(request, bar, user)
    
    if broadcast_portlet.form_success():
        return HttpResponseRedirect(h.internal_url('logged_in', user, {'broadcast_popup_success':1}))
    else:
        return HttpResponseRedirect(h.internal_url('logged_in', user, {'broadcast_popup_success':0}))
    
@login_required
def edit_profile(request, user=0):
    b_user = models.BarUser.for_u_id(user)
    user = b_user.user
    bar = b_user.bar
    edit_processor = EditProfileProcessor(bar, request)
        
    if edit_processor.form_success():
        return HttpResponseRedirect(h.internal_url('logged_in', user, {'selected_tab':e.NavigationTabs.PROFILE.verbose}))
    else:
        return HttpResponse(request)
        #TODO: raise exception here


@login_required    
def remove_menu_item(request, user=0):    
    menu_item = models.MenuItem.for_id(request.POST.getlist('item_id')[0])        
    menu_item.delete()
    
    return HttpResponse(request)    


###API ENDPOINTS###
@api_view(['POST'])
def invite_group(request, coupon=None):
    invitees = request.POST.get('group').split(',')    
    user = models.MobileUser.for_id(request.POST.get('user'))
    
    coup = models.GroupCoupon.for_id(coupon)
    coup.group_invite(user, invitees)

    return HttpResponse()

@api_view(['POST'])
def redeem_coupon(request, coupon=None, type=e.DealTypes.SINGLE):     
    user = request.POST.get('user', None)
    user = models.MobileUser.for_id(user) if user is not None and int(user) > 0 else None
    
    if type == e.DealTypes.SINGLE:
        coup = models.SingleCoupon.for_id(coupon)
        result = coup.redeem_self(user)
    else:
        coup = models.GroupCoupon.for_id(coupon)        
        result = coup.redeem_self(user)

    return render(request, 'portlets/popup_portlets/coupon_response.html', {'success' : result})


class BarViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Bar.objects.all()
    serializer_class = BarSerializer
    

class SingleCouponViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.SingleCoupon.objects.all()
    serializer_class = SingleCouponSerializer


class GroupCouponViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.GroupCoupon.objects.all()
    serializer_class = GroupCouponSerializer
        

class MobileUserViewSet(viewsets.ModelViewSet):
    queryset = models.MobileUser.objects.all()
    serializer_class = MobileUserSerializer        
    
