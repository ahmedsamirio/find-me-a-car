from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.db.models import Avg
from .models import Ad
from .forms import PriceForm, ModelForm

from sklearn.metrics.pairwise import cosine_similarity

from .preprocessing import score_queried_ads, load_features_index, one_hot_encode_features

import pandas as pd
import json

# Create your views here.
def home(request):
    if request.method == 'POST':
        form = PriceForm(request.POST)
        if form.is_valid():
            request.session["min_price"] = form.cleaned_data['min_price']
            request.session["max_price"] = form.cleaned_data['max_price']
            return HttpResponseRedirect('results')
                        
    else:
        price_form = PriceForm()
        model_form = ModelForm()


    return render(request, 'curator/home.html', {'price_form':price_form,
                                                 'model_form':model_form})

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


    features_index = load_features_index()
    ads_features = one_hot_encode_features(queried_ads.drop(columns=["imgs", "description"]), features_index).replace({1: True, 0: False})

    for _, ad_features in ads_features.iterrows():
        print(ad_features)
        for ad_feature in ad_features:
            print(ad_feature)
        break
    # TODO: find the best ads in a given model query and pass them to the template for rendering
    return render(request, 'curator/model.html', {'queried_ads': queried_ads,
                                                  'features': features_index,
                                                  'ads_features': ads_features,
                                                  'model': model})


def load_models(request):
    brand = request.GET.get('brand')
    models = Ad.objects.filter(brand=brand).values_list('model', flat=True).distinct()
    return render(request, 'curator/model_dropdown_list.html', {'models': models})
    