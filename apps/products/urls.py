from django.urls import path
from . import views

urlpatterns = [
    # Product CRUD
    path('menu-builder/product/add/', views.add_product, name='add_product'),
    path('menu-builder/product/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('menu-builder/product/delete/<int:pk>/', views.delete_product, name='delete_product'),
]
