from django.shortcuts import render
from django.http import HttpResponse
from .models import Ad

# Create your views here.
def home(request):
    return HttpResponse("<h1>Find Me A Car!</h1>")

def findbyprice(request):
    """View for user input"""
    # colors = Ad.objects.order_by('color').values_list('color', flat=True).distinct()  # not now
    return render(request, 'curator/findbyprice.html')

def findbymodel(request):
    """View for results"""
    return HttpResponse("<h1>Find Me  A Car by model</h1>")