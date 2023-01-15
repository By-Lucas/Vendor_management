from django import forms

from helpers.validators import allow_only_images_validator

from products.models.category_model import Category
from products.models.product_model import Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']


class ProductForm(forms.ModelForm):
    #image_product = forms.ImageField(validators=[allow_only_images_validator])
    is_available = forms.BooleanField(label='Status do produto', required=False)
    description =forms.CharField(widget=forms.Textarea(attrs={"rows":"3"}))
    class Meta:
        model = Product
        fields = ['category', 'product_title', 'description', 'image_product', 'is_available']