from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.db.models import Avg
from .models import Ad
from .forms import PriceForm

import pandas as pd
import json

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

    # TODO: send the queried_models table to the html file
    return render(request, 'curator/results.html', {'queried_models':queried_models,
                                                    })
        


def model(request):
    """View for results"""
    if request.method == "GET":
        data = request.GET.copy()
    queried_ads = Ad.objects.filter(brand=data['brand']).\
                               filter(model=data['model']).\
                               filter(year=data['year']) 
    model = "{}-{}-{}".format(data['brand'], data['model'], data['year'])# stitch up model name to pass to the template  

    # TODO: find the best ads in a given model query and pass them to the template for rendering
    return render(request, 'curator/model.html', {'queried_ads': queried_ads,
                                                  'model': model})
