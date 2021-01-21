from django import forms
from .models import Ad, Model


class PriceForm(forms.Form):
    min_price = forms.CharField(label="Minimum Price", max_length=100)
    max_price = forms.CharField(label="Maximum Price", max_length=100)


# class ModelForm(forms.Form):
#     brands = [(i+1, x) for i, x in enumerate(Ad.objects.values_list('brand', flat=True).distinct())]
#     brand = forms.ChoiceField(label="Brand", widget=forms.Select, choices=brands)

class ModelForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ('brand', 'model', 'year')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model'].queryset = Model.objects.none()

        if 'brand_id' in self.data:
            try:
                brand_id = int(self.data.get('brand_id'))
                self.fields['model'].queryset = Model.objects.filter(brand_id=brand_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Modella queryset
        elif self.instance.pk:
            self.fields['model'].queryset = self.instance.brand.model_set.order_by('name')


