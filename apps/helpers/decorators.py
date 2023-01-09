from functools import wraps
from django.shortcuts import HttpResponse
from django.contrib import messages
from django.utils.translation import gettext as _
from django.shortcuts import redirect

from helpers import commons
from accounts.models import User
from vendor.model.vendor_models import Vendor

import json


def admin_level_required(view_func):
    def _decorator(request, *args, **kwargs):

        try:
            user_clinic_permission = Vendor.objects.get(user=request.user)

        except Vendor.DoesNotExist:
            user_clinic_permission = Vendor.objects.get(user=request.user)
            user_clinic_permission.user.is_active =  True
            user_clinic_permission.save()

        if user_clinic_permission.user.role == commons.ADMIN_SISTEM or user_clinic_permission.user.is_superuser:
            response = view_func(request, *args, **kwargs)
            return response
        else:
            return HttpResponse(
                status=404,
                headers={
                    'HX-Trigger': json.dumps({
                    "showMessage": "Você não tem permissão pra acessar o recurso"
                    })
                }
            )

    return wraps(view_func)(_decorator)


def vendor_level_required(view_func):
    def _decorator(request, *args, **kwargs):
        try:
            user_clinic_permission = Vendor.objects.get(user=request.user)

        except Vendor.DoesNotExist:
            user_clinic_permission = Vendor.objects.get(user=request.user)
            user_clinic_permission.user.is_active =  True
            user_clinic_permission.save()

        if user_clinic_permission.user.role == commons.VENDOR:
            response = view_func(request, *args, **kwargs)
            return response
        else:
            return HttpResponse(
                status=404,
                headers={
                    'HX-Trigger': json.dumps({
                    "showMessage": "Você não tem permissão pra acessar o recurso"
                    })
                }
            )

    return wraps(view_func)(_decorator)


def customer_level_required(view_func):
    def _decorator(request, *args, **kwargs):
        try:
            user_clinic_permission = Vendor.objects.get(user=request.user)
        except Vendor.DoesNotExist:
            user_clinic_permission = Vendor.objects.get(user=request.user)

        if user_clinic_permission.user.role == commons.ADMIN_SISTEM or user_clinic_permission.user.role == commons.USER_COMMOM or user_clinic_permission.user.is_superuser:

            response = view_func(request, *args, **kwargs)
            return response
        else:
            return HttpResponse(
                status=404,
                headers={
                    'HX-Trigger': json.dumps({
                    "showMessage": "Você não tem permissão pra acessar o recurso"
                    })
                }
            )

    return wraps(view_func)(_decorator)
