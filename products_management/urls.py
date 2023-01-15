from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from apps.products.api.viewsets import ProductViewSet, CategoryListViewSet, ProductDetailViewSet
from apps.accounts.api.viewsets import UserViewSet, UserListViewSet, ProfileUserViewSet


version_api = 'api/v1/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vendor.urls')),
    path('', include('products.urls')),
    path('', include('accounts.urls')),
    path('', include('core.urls')),
] 

router = routers.DefaultRouter()

router.register(r'user', UserViewSet, basename='accounts')
router.register(r'users', UserListViewSet, basename='users')
router.register(r'profile', ProfileUserViewSet, basename='profile')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'category', CategoryListViewSet, basename='category')

urlpatterns += [
    path(version_api, include(router.urls)),
    #path(f'{version_api}product/<int:product_id>', ProductDetailViewSet.as_view()),
    ]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
