from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
import json

from products.forms import ProductForm
from products.models.category_model import Category
from products.models.product_model import Product

from vendor.model.vendor_models import Vendor
from django.contrib import messages

from django.contrib.auth.decorators import login_required, user_passes_test
from helpers.decorators import vendor_level_required, customer_level_required, admin_level_required
from helpers.filters import ProductFilter
from django.template.defaultfilters import slugify


def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor
    

@login_required(login_url='login')
@admin_level_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        image = request.POST['image_product']
        print(image)
        if form.is_valid():
            product_title = form.cleaned_data['product_title']
            product = form.save(commit=False)
            product.slug = slugify(product_title)
            product.save()
            messages.success(request, 'Produto adicionaro com sucesso.')
            return redirect('home')
        else:
            messages.error(request, f'Obteve o seguinte erro: {form.errors}')
            return redirect('home')
    else:
        form = ProductForm()
    context = {
        'form': form,
    }
    return render(request, 'products/add_product.html', context)


@login_required(login_url='login')
@admin_level_required
def edit_product(request, pk=None):
    prod = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=prod)
        if form.is_valid():
            product_title = form.cleaned_data['product_title']
            product = form.save(commit=False)
            product.slug = slugify(product_title)
            form.save()
            messages.success(request, 'Produto atualizado com sucesso.')
            return redirect('home')
        else:
            messages.success(request, f'Obteve o seguinte erro(s): {form.errors}')
            return redirect('home')

    else:
        form = ProductForm(instance=prod)
        
    context = {
        'form': form,
        'prod': prod,
    }
    return render(request, 'products/includes/modal-edit.html', context)

def product_list(request):
    products = Product.objects.all()

    product_filter = ProductFilter(request.GET, queryset=products)

    if not product_filter.qs:
        messages.error(request, 'Nenhum, produto encontrado')

    context = {
            'products': products,
            'product_filter':product_filter
        }
    return render(request, 'products/product-list.html', context)

@login_required(login_url='login')
@admin_level_required
def delete_product(request, pk=None):
    prod = get_object_or_404(Product, pk=pk)
    prod.delete()
    messages.error(request, 'O produto deletado com sucesso!')
    return redirect('home', prod.category.id)

