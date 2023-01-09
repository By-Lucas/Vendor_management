from django.urls import path

from core.views import home, product_list

urlpatterns = [
    path('home', home, name='home'),
    path('produtos', product_list, name='product_list')

]
