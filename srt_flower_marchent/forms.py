from django import forms
from .models import Flower


class FlowerPriceForm(forms.ModelForm):
    class Meta:
        model = Flower
        fields = ('price', 'available_stock', 'image')
        widgets = {
            'price': forms.NumberInput(attrs={'step': '0.01', 'class': 'input-field'}),
            'available_stock': forms.NumberInput(attrs={'class': 'input-field'}),
            'image': forms.ClearableFileInput(attrs={'class': 'input-field'}),
        }
