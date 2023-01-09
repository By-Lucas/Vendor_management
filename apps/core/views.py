from django.shortcuts import redirect, render
from helpers.decorators import customer_level_required
from django.core.paginator import Paginator, InvalidPage
from django.db.models import Q

# Alert message
from django.contrib import messages
from django.contrib.messages import constants

from products.models.product_model import Product
from products.models.category_model import Category

from helpers.filters import ProductFilter


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

def product_list(request):
    category= Category.objects.all()
    products= Product.objects.all()

    product_filter = ProductFilter(request.GET, queryset=products)

    if not product_filter.qs:
        messages.error(request, 'Nenhum, produto encontrado')

    # Paginator
    ITEMS_PER_PAGE = 8
    page = request.GET.get('page')
    paginator = Paginator(products, ITEMS_PER_PAGE)
    total = paginator.count
    products = paginator.get_page(page)
    try:
        products_pages = paginator.page(page)
    except InvalidPage:
        products_pages = paginator.page(1)

    context = {
            'products': products,
            'products_pages': products_pages,
            'product_filter':product_filter
        }

    return render(request, 'products/product-list.html', context)

