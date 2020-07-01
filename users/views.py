from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import ListView

from .forms import CreateUserForm
from django.urls import reverse_lazy
from django.views import generic
from .models import Profile


class SignUp(generic.CreateView):
    form_class = CreateUserForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def form_valid(self, form):
        data = form.cleaned_data
        print(data)
        user = User.objects.create_user(username=data['username'],
                                        password=data['password'],
                                        first_name=data['first_name'],
                                        last_name=data['last_name'],
                                        email=data['email'],

                                        )
        profile = Profile.objects.create(user=user,
                                         profile_picture=data['profile_picture'],
                                         )

        return redirect('login')


class AllProfile(ListView):
    model = Profile
    context_object_name = 'all_profiles'
    template_name = 'profile_list.html'


class Profile(ListView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'profile.html'

