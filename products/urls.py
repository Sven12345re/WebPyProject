from django.urls import path, reverse
from . import views
from django.conf import settings

urlpatterns = [
    path('show/', views.product_list, name='product-list'),
    path('show/<int:pk>/', views.product_detail, name='product-detail'),
    path('show/<int:pk>/vote/<str:up_or_down>/', views.vote, name='product-vote'),
    # path('show/<int:pk>/vote/<str:Report>/', views.report, name='report-vote'),
    path('add/', views.ProductCreateView.as_view(), name='product-create'),
    # path('show/<int:pk>/like/<str:Like_or_not>/', views.like, name='comment-vote'),
    path('show/<int:pk>/like/<int:comment_pk>/<str:Like_or_not>/', views.like, name='comment-vote'),
    path('show/<int:pk>/vote/<int:comment_pk>/<str:report>/', views.report, name='report-vote'),
    path('search/', views.product_search, name='product-search'),
    path('manager/', views.manager_portal, name='manager-portal'),
    path('delete/<int:pk>', views.comment_delete, name='delete'),
    path('update/<int:pk>', views.comment_update, name='update'),
    path('deleteManager/<int:pk>', views.comment_delete_manager, name='deleteManager'),
    path('updateManager/<int:pk>', views.comment_update_manager, name='updateManager'),
    path('deleteManagerproduct/<int:pk>', views.delete_product_manager, name='deleteManagerproduct'),
   # path('EditManagerproduct/<int:pk>', views.edit_product_manager, name='editManagerproduct'),
    path('addProductPhoto/<int:pk>', views.add_product_photo_manager, name='addProductPhotoManager')


]
