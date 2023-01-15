from rest_framework import serializers

from products.models.product_model import Product
from products.models.category_model import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name', 'description']


class ProductSerializer(serializers.ModelSerializer):
    #category_set = CategorySerializer(many=True)
    class Meta:
        model = Product
        fields = ['category', 'product_title', 'description', 'image_product', 'is_available']

