from rest_framework import serializers

from vendor.model.vendor_models import Vendor
from vendor.model.product_value_model import VendorProductValue


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'user', 'user_profile', 'vendor_name', 'vendor_slug', 'is_approved']


class VendorValueSerializer(serializers.ModelSerializer):
    #vendor_set = CategorySerializer(many=True)
    class Meta:
        model = VendorProductValue
        fields = ['id', 'vendor', 'product', 'price_product']

