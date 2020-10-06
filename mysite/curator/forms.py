from django import forms
from .models import Ad

class PriceForm(forms.Form):
    min_price = forms.CharField(label="Minimum Price", max_length=100)
    max_price = forms.CharField(label="Maximum Price", max_length=100)


class ModelForm(forms.Form):
    brands = [(i+1, x) for i, x in enumerate(Ad.objects.values_list('brand', flat=True).distinct())]
    brand = forms.ChoiceField(label="Brand", widget=forms.Select, choices=brands)

# class ModelForm(forms.ModelForm):
#     class Meta:
#         model = Ad
#         fields = ('brand', 'model', 'year')


#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['brand'].queryset = Ad.objects.values_list('brand', flat=True).distinct() 
