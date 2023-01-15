from rest_framework import viewsets
from rest_framework import permissions, authentication

from vendor.api.serializers import VendorValueSerializer, VendorSerializer
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
    