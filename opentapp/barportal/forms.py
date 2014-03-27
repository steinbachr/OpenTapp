from django.contrib.auth import authenticate
from django import forms
from django.forms import ModelForm
from django.forms.widgets import DateInput
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from barportal.models import Bar
from barportal.form_fields import *
import enums as enums
import helpers as h
import re, datetime


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder' : "User Name", 'required' : 'true'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : "Password", 'required' : 'true'}, render_value=False), required=True)
    
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()        
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            pass #do nothing, user supplied correct credentials
        else:
            raise forms.ValidationError(u'Bar/Password doesn\'t match!')                        
        
        return cleaned_data
    

class BarSignupForm(ModelForm):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), required=True)
    email = forms.EmailField(required=True)
    form_name = forms.CharField(required=False, widget=forms.HiddenInput(), label='')
    #fields we have to add because they're customized
    address = forms.CharField(required=True, widget=forms.TextInput(attrs={'class' : 'bar-location'}))
    hours_from = AppTimeField(required=False)
    hours_to = AppTimeField(required=False)
    kitchen_hours_from = AppTimeField(required=False)
    kitchen_hours_to = AppTimeField(required=False)

    class Meta:
        model = Bar
        exclude = ['longitude', 'latitude', 'bar_tz', 'rating']

    def clean(self):
            cleaned_data = super(BarSignupForm, self).clean()        
            username = cleaned_data.get('username')
                
            try:
                user = User.objects.get(username=username)
                raise forms.ValidationError(u'Username already taken! Please choose another') #raise error, shouldn't have duplicate usernames
            except ObjectDoesNotExist:
                pass
            
            return cleaned_data
        
    def basic_info(self):
        return (self['username'], self['password'], self['email'])
    
    def additional_info(self):
        return [field for field in self if field.name not in ('username', 'password', 'email')]

        
class BroadcastCouponForm(forms.Form):
    deal_type = forms.ChoiceField(required=True, choices=enums.DealTypes.list_for_dropdown(), widget=forms.Select(attrs={'class': 'deal-type-select'}))            
    coupon_valid_from_date = AppDateField(required=True)        
    coupon_valid_to_date = AppDateField(required=True)
    coupon_valid_from_time = AppTimeField(required=True)
    coupon_valid_to_time = AppTimeField(required=True)
    valid_all_day = forms.BooleanField(required=False, label="all day")
    one_per_customer = forms.BooleanField(required=False, label="limit one per customer?")
 
class BroadcastSingleCouponForm(BroadcastCouponForm):
    coupon_description = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'coupon-description'}))
    
class BroadcastGroupCouponForm(BroadcastCouponForm):
    tier_one_min = forms.CharField(required=True, widget=forms.HiddenInput(attrs={'class':'min-range'}))
    tier_one_max = forms.CharField(required=True, widget=forms.HiddenInput(attrs={'class':'max-range'}))
    tier_one_desc = forms.CharField(required=True, widget=forms.TextInput())
    tier_two_min = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'class':'min-range'}))
    tier_two_max = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'class':'max-range'}))
    tier_two_desc = forms.CharField(required=False, widget=forms.TextInput())
    

class EditBarForm(ModelForm):
    hours_from = AppTimeField(required=False)
    hours_to = AppTimeField(required=False)
    kitchen_hours_from = AppTimeField(required=False)
    kitchen_hours_to = AppTimeField(required=False)
    
    class Meta:
        model = Bar
        exclude = ['longitude', 'latitude', 'address', 'name', 'bar_tz', 'raw_menu', 'rating']        
          

    def handle_uploaded_file(f):
        with open('some/file/name.txt', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
