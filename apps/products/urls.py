from django.urls import path, include

from . import views
from products.api.viewsets import ProductViewSet


urlpatterns = [
    path('menu-builder/products/', views.product_list, name='product_list'),
    path('menu-builder/product/add/', views.add_product, name='add_product'),
    path('menu-builder/product/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('menu-builder/product/delete/<int:pk>/', views.delete_product, name='delete_product'),
]
