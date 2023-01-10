from django.shortcuts import redirect, render
from helpers.decorators import customer_level_required
from django.core.paginator import Paginator, InvalidPage
from django.db.models import Q

# Alert message
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required, user_passes_test

from products.models.product_model import Product
from products.models.category_model import Category
from helpers.filters import ProductFilter
from helpers.decorators import vendor_level_required, customer_level_required, admin_level_required


def home(request):
    template_name = 'core/home.html'
    products= Product.objects.all()

    product_filter = ProductFilter(request.GET, queryset=products)

    if not product_filter.qs:
        messages.error(request, 'Nenhum, produto encontrado')

    context = {
        'product_filter':product_filter
    }
    return render(request, template_name, context)
    