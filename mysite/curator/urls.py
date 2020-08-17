from django.urls import path
from . import views

app_name = 'curator'

urlpatterns = [
    path('', views.home, name='home'),
    path('price', views.findbyprice, name='price'),
    path('model', views.findbymodel, name='model'),
]