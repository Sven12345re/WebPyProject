from django import forms
from django.contrib.auth.models import User


class CreateUserForm(forms.ModelForm):
    profile_picture = forms.ImageField()

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }
