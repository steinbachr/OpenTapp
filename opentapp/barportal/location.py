from geopy.geocoders.googlev3 import GoogleV3
from barwatch import helpers as h
import httplib
import urllib2 as url
import json

class BarLocation():        
    @classmethod
    def geocode_address(cls, address):
        '''a method to convert an address in string representation to its lat, long form'''
        g = GoogleV3()
        place, (lat, lng) = g.geocode(address, exactly_one=True)    #this is a REALLY naive implementation TODO: make picking location smarter by verifying address with user on submit
                
        return (lat, lng)
    
    @classmethod
    def reverse_geocode(cls, lat_lng):
        '''a method to create an address out of its latitude and longitude'''
        g = geocoders.Google()
        (place, point) = g.reverse(lat_lng)
        return place
    
    @classmethod
    def timezone_by_lat_lng(cls, lat_lng):
        '''a method to get the timezone based on latitude longitude pair'''
        config = h.parse_config_file()
        request_url = config['api_timezone_url']
        request_user = config['geonames_user']
        params = {'lat':lat_lng[0],'lng':lat_lng[1],'username':request_user}
        
        request = url.Request(h.external_url(request_url, params=params))
        response = url.urlopen(request)
        
        timezone_json = response.read()
        timezone = json.loads(timezone_json)['timezoneId']
        
        return timezone
        
                
        
        
