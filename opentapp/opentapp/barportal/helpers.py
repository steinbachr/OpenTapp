import string
import random
import datetime, re, os
from django.core.urlresolvers import reverse
from pytz import timezone
from opentapp.barportal import enums as e

def random_string(n):
    '''generate a random string of n characters'''
    lst = [random.choice(string.ascii_letters + string.digits) for char in range(n)]
    str = "".join(lst)
    return str

###DATE/TIME STUFF###
def get_now():
    return datetime.datetime.utcnow().replace(tzinfo=timezone('UTC'))

def time_delta(time_1, time_2, in_seconds=False):
    '''a function to get the difference in time betwen two times'''    
    diff = time_1 - time_2     
    return diff.total_seconds() if in_seconds else diff.days

def combine_date_time(date, time):
    '''a function to combine a date and time into a datetime obj'''
    return datetime.datetime.combine(date, time)

def date_from_string(d_string):
    format = e.Formatting.DATE_FORMAT
    return datetime.datetime.strptime(d_string,format).date()

def time_from_string(t_string):
    format = e.Formatting.TIME_FORMAT
    return datetime.datetime.strptime(t_string,format).time()

def string_from_time(t):
    format = e.Formatting.TIME_FORMAT
    return datetime.time.strftime(t, format)


def string_from_date(d):
    format = e.Formatting.DATE_FORMAT
    return datetime.date.strftime(d, format)
###END DATE STUFF###
    
###FILE STUFF###
def parse_config_file():    
    config_dict = {}    

    with open('{base}/config.ini'.format(base=os.path.dirname(os.path.dirname(__file__))), 'r') as file:
        for line in file.readlines():
            if line.startswith('#'):
                continue
            match = line.split('=')
            config_dict[match[0]] = match[1].rstrip()
            
    return config_dict

def read_file(file_path):
    contents = ''
    with open(file_path, 'r') as file:        
        for line in file.readlines():
            contents += line
            
    return contents

def admin_emails():
    emails = parse_config_file().get('admin_emails')
    return emails.split(',')
###END FILE STUFF###

###URL STUFF###
def external_url(url_string, params=None):                    
    external_url = url(url_string, params)        
    return external_url

def internal_url(view_action, user, params=None, action_dir='views'):       
    internal_url = url(reverse('opentapp.barportal.%s.%s' % (action_dir, view_action), args=(user.id,)), params)
    return internal_url
        
def url(url, params):
    params_string = '?%s' % ''.join(['%s=%s&' % (key, value) for (key, value) in params.items()] if params is not None else '') .rstrip('&')
    final_url = url + params_string
    return final_url
###END URL###  

###GCM STUFF###
def send_gcm_message(ids, dat):
    from gcm import GCM
    
    gcm = GCM(e.API_KEYS.GOOGLE_API)    
    
    response = gcm.json_request(registration_ids=ids, data=dat)

    if 'errors' in response:
        for error, reg_ids in response['errors'].items():
            #TODO: do something better here
            print "THE ERROR IS", error
    
###END GCM STUFF###
    
    
