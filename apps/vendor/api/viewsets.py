from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, authentication
from rest_framework import status

from vendor.api.serializers import VendorValueSerializer, VendorSerializer
from accounts.models import User
from vendor.model.vendor_models import Vendor
from vendor.model.product_value_model import VendorProductValue


class VendorViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]
    serializer_class = VendorSerializer

    def get_queryset(self):
        query = Vendor.objects.all()
        return query


class VendorValueViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]
    serializer_class = VendorValueSerializer

    def get_queryset(self):
        query = VendorProductValue.objects.all()
        return query
    