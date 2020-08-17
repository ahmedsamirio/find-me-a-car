from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("<h1>Find Me A Car!</h1>")

def input(request):
    """View for user input"""
    return HttpResponse("<h1>User input view</h1>")

def result(request):
    """View for results"""
    return HttpResponse("<h1>Results</h1>")