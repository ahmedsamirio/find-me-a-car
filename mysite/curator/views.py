from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.db.models import Avg
from .models import Ad
from .forms import PriceForm

import pandas as pd

# Create your views here.
def home(request):
    return HttpResponse("<h1>Find Me A Car!</h1>")

def findbyprice(request):
    """View for user input"""
    if request.method == 'POST':
        form = PriceForm(request.POST)
        if form.is_valid():
            request.session["min_price"] = form.cleaned_data['min_price']
            request.session["max_price"] = form.cleaned_data['max_price']
            return HttpResponseRedirect('results')
                        
    else:
        form = PriceForm()

    return render(request, 'curator/findbyprice.html', {'form':form})

def price_results(request):
    if request.session.has_key("min_price"):
        min_price = request.session["min_price"]
    if request.session.has_key("max_price"):
        max_price = request.session["max_price"]
    queried_models = Ad.objects.values('brand', 'model', 'year').\
                                        annotate(mean_price=Avg('price')).\
                                        filter(mean_price__gte=min_price).\
                                        filter(mean_price__lte=max_price) 
    return render(request, 'curator/results.html', {'min_price':min_price,
                                                    'max_price':max_price})
        


def findbymodel(request):
    """View for results"""
    return HttpResponse("<h1>Find Me  A Car by model</h1>")