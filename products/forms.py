from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'Desc', 'Img', 'type', 'date_published']
        widgets = {
            'user': forms.HiddenInput(),
        }
