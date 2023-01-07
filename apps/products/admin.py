from django.contrib import admin

from products.models.category_model import Category
from products.models.product_model import Product


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name',  'updated_at')
    search_fields = ('category_name',)


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_title',)}
    list_display = ('product_title', 'category', 'is_available', 'updated_at')
    search_fields = ('product_title', 'category__category_name')
    list_filter = ('is_available',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)