from django.conf import settings

from accounts.others_models.model_profile import UserProfile
from vendor.model.vendor_models import Vendor
from products.models.category_model import Category


def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor=vendor)

def get_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = None
    return dict(user_profile=user_profile)

def get_categories(request):
    try:
        category = Category.objects.all()
    except:
        category = None
    return dict(category=category)
