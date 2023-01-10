from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
import json

from products.forms import ProductForm
from products.models.category_model import Category
from products.models.product_model import Product

from vendor.model.vendor_models import Vendor
from django.contrib import messages

from django.contrib.auth.decorators import login_required, user_passes_test
from helpers.decorators import vendor_level_required, customer_level_required, admin_level_required
from django.template.defaultfilters import slugify


def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor

@login_required(login_url='login')
@admin_level_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
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
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                    "ProductListChanged": None,
                    "showMessage": f"Produto {product} editado com sucesso.."
                    })
                }
            )
        else:
            print(form.errors)

    else:
        form = ProductForm(instance=prod)
        
    context = {
        'form': form,
        'prod': prod,
    }
    return render(request, 'products/edit_product.html', context)

@login_required(login_url='login')
@admin_level_required
def delete_product(request, pk=None):
    prod = get_object_or_404(Product, pk=pk)
    prod.delete()
    messages.success(request, 'O produto excluído com sucesso!')
    return redirect('product_by_category', prod.category.id)

