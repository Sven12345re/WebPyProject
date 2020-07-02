from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('show/', views.ProductListView.as_view(), name='product-list'),
    path('show/<int:pk>/', views.product_detail, name='product-detail'),
    path('show/<int:pk>/vote/<str:up_or_down>/', views.vote, name='product-vote'),
    path('add/', views.ProductCreateView.as_view(), name='product-create'),

]

