from functools import wraps
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect

from helpers import commons
from accounts.models import User
from vendor.model.vendor_models import Vendor


def admin_level_required(view_func):
    def _decorator(request, *args, **kwargs):
        if request.user.is_superuser :
            response = view_func(request, *args, **kwargs)
            return response
        try:
            user_clinic_permission = Vendor.objects.get(user=request.user, user__is_active=True)

        except Vendor.MultipleObjectsReturned or Vendor.DoesNotExist:
            user_clinic_permission = Vendor.objects.filter(user=request.user, user__is_active=True).first()
            
        if user_clinic_permission.user.role == commons.ADMIN_SISTEM:
            response = view_func(request, *args, **kwargs)
            return response
        else:
            messages.warning(request, _('Você não tem permissão pra acessar o recurso'))
            return redirect('home')

    return wraps(view_func)(_decorator)


def vendor_level_required(view_func):
    def _decorator(request, *args, **kwargs):
        if request.user.is_superuser :
            response = view_func(request, *args, **kwargs)
            return response
        try:
            user_clinic_permission = Vendor.objects.get(user=request.user, user__is_active=True)

        except Vendor.MultipleObjectsReturned or Vendor.DoesNotExist:
            user_clinic_permission = Vendor.objects.filter(user=request.user, user__is_active=True).first()

        if user_clinic_permission.user.role == commons.VENDOR or user_clinic_permission.user.role == commons.ADMIN_SISTEM:
            response = view_func(request, *args, **kwargs)
            return response
        else:
            messages.warning(request, _('Você não tem permissão pra acessar o recurso'))
            return redirect('home')

    return wraps(view_func)(_decorator)


def customer_level_required(view_func):
    def _decorator(request, *args, **kwargs):
        if request.user.is_superuser :
            response = view_func(request, *args, **kwargs)
            return response

        try:
            user_clinic_permission = Vendor.objects.get(user=request.user, user__is_active=True)

        except Vendor.MultipleObjectsReturned or Vendor.DoesNotExist:
            user_clinic_permission = Vendor.objects.filter(user=request.user, user__is_active=True).first()

        if user_clinic_permission.user.role == commons.ADMIN_SISTEM or request.user.role == commons.USER_COMMOM:
            response = view_func(request, *args, **kwargs)
            return response
        else:
            messages.warning(request, _('Você não tem permissão pra acessar o recurso'))
            return redirect('home')

    return wraps(view_func)(_decorator)
