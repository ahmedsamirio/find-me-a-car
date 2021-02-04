from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.db.models import Avg
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy

from .models import Ad, Model, Brand
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
    queried_models = Ad.objects.all().\
                        annotate(mean_price=Avg('price')).\
                        filter(mean_price__gte=min_price).\
                        filter(mean_price__lte=max_price) 

    # TODO: send the queried_models table to the html file
    return render(request, 'curator/results.html', {'queried_models':queried_models,
                                                    })



def model(request):
    """View for results"""
    if request.method == "POST":
        data = request.POST.copy()

    query = str(Ad.objects.all().query)
    queried_ads = pd.read_sql_query(query, connection)

    print('Before Querying Shape:', queried_ads.shape)

    queried_ads.drop_duplicates(inplace=True)

    # print(data["model"], Model.objects.filter(name=data["model"]))
    # model_id = Model.objects.filter(name=data["model"])[0].id
    # brand_id = Brand.objects.filter(name=data["brand"])[0].id

    brand_id = int(data['brand'])
    model_id = int(data['model'])

    mask = (queried_ads.brand_id == brand_id) & (queried_ads.model_id == model_id) &\
           (queried_ads.year.astype(int) <= int(data['max_year'])) &\
           (queried_ads.year.astype(int) >= int(data['min_year']))
    queried_ads = queried_ads[mask]

    print(data['brand'], data['model'])

    brand = Brand.objects.filter(id=data['brand'])[0].name
    model = Model.objects.filter(id=data['model'])[0].name

    model = "{}-{}".format(brand, model) # stitch up model name to pass to the template  

    print('Querying Shape:', queried_ads.shape)

    sorted_indices = score_queried_ads(queried_ads)
    queried_ads = queried_ads.iloc[sorted_indices]


    features_index = load_features_index()
    ads_features = one_hot_encode_features(queried_ads.drop(columns=["imgs", "description"]), features_index).replace({1: True, 0: False})

    for _, ad_features in ads_features.iterrows():
        print(ad_features)
        for ad_feature in ad_features:
            print(ad_feature)
        break

    queried_ads_and_features = [(ad, ad_features) for ad, (_, ad_features) in zip(queried_ads.itertuples(), ads_features.iterrows())]

    # TODO: find the best ads in a given model query and pass them to the template for rendering
    return render(request, 'curator/model.html', {'queried_ads_and_features': queried_ads_and_features,
                                                  'features': features_index,
                                                  'model': model})


def load_models(request):
    brand_id = request.GET.get('brand_id')
    models = Model.objects.filter(brand_id=brand_id).order_by('name')
    return render(request, 'curator/models_dropdown_list.html', {'models': models})
    
