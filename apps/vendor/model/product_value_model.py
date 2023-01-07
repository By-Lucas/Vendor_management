from django.db import models
from django.db.models.fields.related import OneToOneField

from vendor.model.vendor_models import Vendor
from products.models.product_model import Product


class VendorProductValue(models.Model):
    vendo = OneToOneField(Vendor, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    price_product = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.product.product_title
    
    class Meta:
        verbose_name = 'Preço do produto'
        verbose_name_plural = 'Preço do produtos'