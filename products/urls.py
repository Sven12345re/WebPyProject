from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('show/', views.product_list, name='product-list'),
    path('show/<int:pk>/', views.product_detail, name='product-detail'),
    path('show/<int:pk>/vote/<str:up_or_down>/', views.vote, name='product-vote'),
    path('show/<int:pk>/vote/<str:Report>/', views.report, name='report-vote'),
    path('add/', views.ProductCreateView.as_view(), name='product-create'),
    path('show/<int:pk>/like/<int:comment_pk>/<str:Like_or_not>/', views.like, name='comment-vote'),
    path('search/', views.product_search, name='product-search'),

]
