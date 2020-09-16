from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.db.models import Avg
from .models import Ad
from .forms import PriceForm

from sklearn.metrics.pairwise import cosine_similarity

from .preprocessing import score_queried_ads

import pandas as pd
import json

# Create your views here.
def home(request):
    return render(request, 'curator/home.html')

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

    query = str(Ad.objects.all().query)
    queried_ads = pd.read_sql_query(query, connection)

    queried_ads.drop_duplicates(inplace=True)

    mask = (queried_ads.brand == data["brand"]) & (queried_ads.model == data["model"]) & (queried_ads.year == int(data["year"]))
    queried_ads = queried_ads[mask]

    model = "{}-{}-{}".format(data['brand'], data['model'], data['year'])# stitch up model name to pass to the template  

    sorted_indices = score_queried_ads(queried_ads)
    queried_ads = queried_ads.iloc[sorted_indices]

    for _, row in queried_ads.iterrows():
        print(row)

    # TODO: find the best ads in a given model query and pass them to the template for rendering
    return render(request, 'curator/model.html', {'queried_ads': queried_ads,
                                                  'model': model})
