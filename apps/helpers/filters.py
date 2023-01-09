import django_filters
from django import forms

from products.models.product_model import Product

class ProductFilter(django_filters.FilterSet):
    product_title = django_filters.CharFilter(label="Nome do produto ", lookup_expr='icontains', widget=forms.TextInput(
            attrs={
                'class':'form-control','placeholder': 'Digite o nome do produto'
            }
        ))

    class Meta:
        model = Product
        fields = ['category', 'product_title']