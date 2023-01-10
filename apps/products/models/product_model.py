from django.db import models
from django.urls import reverse
from PIL import Image

from products.models.category_model import Category

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    product_title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    image_product = models.FileField(upload_to='product', blank=True, null=True)
    is_available = models.BooleanField(verbose_name='Produto ativo', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_title

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

