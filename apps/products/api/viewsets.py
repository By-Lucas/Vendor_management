from rest_framework import generics, viewsets
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import permissions, authentication
from rest_framework import status

from products.api.serializers import ProductSerializer, CategorySerializer
from accounts.models import User
from products.models.product_model import Product
from products.models.category_model import Category


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('category', 'product_title')

    def get_queryset(self):
        query = Product.objects.all()
        return query
    

class ProductDetailViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]

    def get_object(self, product_id):
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return None

    def get(self, request, product_id, *args, **kwargs):
     
        product_instance = self.get_object(product_id)
        if not product_instance:
            return Response(
                {"res": "Produto não existe"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ProductSerializer(product_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, product_id, *args, **kwargs):
        product_instance = self.get_object(product_id)
        if not product_instance:
            return Response(
                {"res": "Produto não existe"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ProductSerializer(instance=product_instance, data=request.data, partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id, *args, **kwargs):
        product_instance = self.get_object(product_id)
        if not product_instance:
            return Response(
                {"res": "Produto não existe"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        product_instance.delete()
        return Response(
            {"res": "Produto dedeletado!"},
            status=status.HTTP_200_OK
        )


class CategoryListViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]
    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset
    serializer_class = CategorySerializer


class ProfileUserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        queryset = Product.objects.filter(user=self.request.user)
        print(self.request.user.id)
        return queryset
    serializer_class = Category
