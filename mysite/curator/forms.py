from django import forms

class PriceForm(forms.Form):
    min_price = forms.CharField(label="Minimum Price", max_length=100)
    max_price = forms.CharField(label="Maximum Price", max_length=100)
