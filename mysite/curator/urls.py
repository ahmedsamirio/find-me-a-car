from django.urls import path
from . import views

app_name = 'curator'

urlpatterns = [
    path('', views.home, name='home'),
    path('inputs', views.input, name='input'),
    path('results', views.result, name='result'),
]