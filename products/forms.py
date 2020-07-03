from django import forms
from .models import Product,Comment


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'Desc', 'Img', 'type', 'date_published' ,'document']
        widgets = {
            'user': forms.HiddenInput(),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text' ,'rate']
        widgets = {
            'user': forms.HiddenInput(),
            'book': forms.HiddenInput(),
        }
