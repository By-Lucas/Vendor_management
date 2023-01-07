from django.contrib import admin
from vendor.model.vendor_models import Vendor
from vendor.model.product_value_model import VendorProductValue


class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'vendor_name', 'is_approved', 'created_at')
    list_display_links = ('user', 'vendor_name')
    list_editable = ('is_approved',)


class VendorProductValueAdmin(admin.ModelAdmin):
    list_display = ('product', 'price_product')
    list_display_links = ('product',)


admin.site.register(Vendor, VendorAdmin)
admin.site.register(VendorProductValue, VendorProductValueAdmin)