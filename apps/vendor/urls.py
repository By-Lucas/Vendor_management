from django.urls import path, include
from . import views
from accounts import views as AccountViews


urlpatterns = [
   # path('', AccountViews.vendorDashboard, name='vendor'),
    path('profile/', views.vprofile, name='vprofile'),
    path('menu-builder/', views.menu_builder, name='menu_builder'),
    path('menu-builder/category/<int:pk>/', views.productitems_by_category, name='product_by_category'),

    # Category CRUD
    path('menu-builder/category/add/', views.add_category, name='add_category'),
    path('menu-builder/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('menu-builder/category/delete/<int:pk>/', views.delete_category, name='delete_category'),

    # Products Vendors
    path('menu-builder/vendors/products/<int:pk>', views.get_product_vendors, name='get_product_vendors'),

]