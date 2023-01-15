from django.urls import path, include
from rest_framework import routers
from decouple import config

from .views import views
from accounts.api.viewsets import UserViewSet, UserListViewSet, ProfileUserViewSet

version_api = 'api/v1/'

urlpatterns = [
   path('', views.myAccount),
    path('cadastrar-usuario/', views.registerUser, name='registerUser'),
    path('cadastrar-fornecedor/', views.registerVendor, name='registerVendor'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('myAccount/', views.myAccount, name='myAccount'),
    path('perfil/', views.ProfileUpdateView.as_view(), name='user_profile'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),
]


router = routers.DefaultRouter()
router.register(r'user', UserViewSet, basename='accounts')
router.register(r'users', UserListViewSet, basename='users')
router.register(r'profile', ProfileUserViewSet, basename='profile')

# ROUTERS API
urlpatterns += [path(version_api, include(router.urls))]