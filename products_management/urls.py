from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from apps.products.api.viewsets import ProductViewSet, CategoryListViewSet, ProductDetailViewSet
from apps.accounts.api.viewsets import UserViewSet, UserListViewSet, ProfileUserViewSet
from apps.vendor.api.viewsets import VendorViewSet, VendorValueViewSet

version_api = 'api/v1/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vendor.urls')),
    path('', include('products.urls')),
    path('', include('accounts.urls')),
    path('', include('core.urls')),
] 

class GestaoDeFornecedores(routers.APIRootView):
    """
    Api para gerenciar fornecedores, e listar os melhores preços
    """
    pass

class DocumentedRouter(routers.DefaultRouter):
    APIRootView = GestaoDeFornecedores

router = DocumentedRouter()

router.register(r'user', UserViewSet, basename='Usuário')
router.register(r'users', UserListViewSet, basename='Usuários')
router.register(r'user-profile', ProfileUserViewSet, basename='Perfil do usuário')
router.register(r'products', ProductViewSet, basename='Produtos')
router.register(r'category', CategoryListViewSet, basename='Categorias')
router.register(r'vendor', VendorViewSet, basename='Fornecedores')
router.register(r'vendor-product-value', VendorValueViewSet, basename='Registar preço produtos')


urlpatterns += [
    path(version_api, include(router.urls)),
    path(f'{version_api}products/<int:product_id>', ProductDetailViewSet.as_view()),
    ]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
