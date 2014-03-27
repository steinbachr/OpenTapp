from barwatch.barportal.models import *
from barwatch.barportal.forms import *
from barwatch.barportal.portlets import *
from barwatch import enums as e
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

def autocompleter(request):
    bar = Bar.for_id(request.session['bar_id'])    
    term = request.GET.get('term', None)    
    
    if bar.has_menu and term:
        menu = Menu.objects.filter(bar=bar).get()        
        return HttpResponse([item.name for item in menu.menu_items])
    
    return HttpResponse(request)    #we dont want to get here
