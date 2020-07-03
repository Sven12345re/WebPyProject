from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('allProfile/', views.AllProfile.as_view(), name='allProfile'),
    path('profile/', views.ProfileView.as_view(), name='profile'),

]
