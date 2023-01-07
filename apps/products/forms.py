from django import forms

from helpers.validators import allow_only_images_validator

from products.models.category_model import Category
from products.models.product_model import Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']


class ProductForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info w-100'}), validators=[allow_only_images_validator])
    class Meta:
        model = Product
        fields = ['category', 'product_title', 'description', 'image', 'is_available']