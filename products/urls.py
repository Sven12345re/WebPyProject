from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('show/', views.ProductListView.as_view(), name='product-list'),
    path('show/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('add/', views.ProductCreateView.as_view(), name='product-create'),

]

