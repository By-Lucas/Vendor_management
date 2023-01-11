from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy, reverse

from products.forms import CategoryForm, ProductForm
from vendor.forms import VendorForm
from accounts.forms import UserProfileForm

from accounts.others_models.model_profile import UserProfile
from products.models.category_model import Category
from products.models.product_model import Product
from vendor.model.vendor_models import Vendor
from vendor.model.product_value_model import VendorProductValue

from helpers.decorators import vendor_level_required, customer_level_required, admin_level_required


def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor

@login_required(login_url='accounts:login')
@vendor_level_required
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Configurações atualizadas.')
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)

    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/vprofile.html', context)

@login_required(login_url='login')
@admin_level_required
def menu_builder(request):
    categories = Category.objects.all().order_by('created_at')
    context = {
        'categories': categories,
    }
    return render(request, 'vendor/category-list.html', context)

@login_required(login_url='login')
#@admin_level_required
def productitems_by_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    productitems = Product.objects.filter(category=category)
    context = {
        'productitems': productitems,
        'category': category,
    }
    return render(request, 'vendor/productitems_by_category.html', context)

@login_required(login_url='login')
@admin_level_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        print(form)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.slug = slugify(category_name)+'-'+str(category.id) # chicken-15
            category.save()
            messages.success(request, 'Categoria adicionada com sucesso!')
            return redirect('product_list')
        else:
            print(form.errors)
            messages.error(request, f'Obteve o seguinte erro: {form.errors}')
            return redirect('product_list')

    else:
        form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'vendor/add_category.html', context)

@login_required(login_url='login')
@admin_level_required
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            #category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Categoria atualizada com sucesso!')
            return redirect('menu_builder')
        else:
            print(form.errors)

    else:
        form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'vendor/edit_category.html', context)

@login_required(login_url='login')
@admin_level_required
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'A categoria foi excluída com sucesso!')
    return redirect('menu_builder')

@login_required(login_url='login')
def get_product_vendors(request, pk=None):
    prod = get_object_or_404(Product, pk=pk)
    product_vendor = VendorProductValue.objects.filter(product=prod)
        
    context = {
        'product_vendor': product_vendor,
        'prod': prod,
    }
    return render(request, 'products/product_vendors.html', context)