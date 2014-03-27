from django import forms
import barwatch.helpers as h
import barwatch.enums as e

class AppTimeField(forms.Field):
    '''
        in the site, time fields are represented as CharFields for display on the front end but should always
        be used as Python Time Objects on the back end, this is why this field is being created
    '''
    def __init__(self, *args, **kwargs):
        super(AppTimeField, self).__init__(*args, **kwargs)
        self.widget = forms.TextInput(attrs={'class':'time-select'})
    
    def to_python(self, value):
        '''normalize time strings to time objects'''
        return h.time_from_string(value)
    
class AppDateField(forms.Field):
    '''
        see AppTimeField description
    '''
    def __init__(self, *args, **kwargs):
        super(AppDateField, self).__init__(*args, **kwargs)
        self.widget = forms.DateInput(format=e.Formatting.DATE_FORMAT, attrs={'class': 'date-select'})

    def to_python(self, value):
        '''normalize date strings to date objects'''
        return h.date_from_string(value)

    
