from rest_framework import generics, viewsets
from rest_framework.views import APIView
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
    
    def put(self, request, product_id, *args, **kwargs):
    
        product_instance = self.get_object(product_id)
        if not product_instance:
            return Response(
                {"res": "Produto não existe"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        data = {
            'category': request.data.get('category'), 
            'product_title': request.data.get('product_title'),
            'description': request.data.get('description'),
            'image_product': request.data.get('image_product'),
            'is_available': request.data.get('is_available'),
        }
        serializer = ProductSerializer(instance=product_instance, data=data, partial = True)
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
