from rest_framework import generics, viewsets
from rest_framework import permissions, authentication

from accounts.api.serializers import UserSerializer, UserProfileSerializer
from accounts.models import User
from accounts.others_models.model_profile import UserProfile


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    def get_queryset(self, format=None):
        query = User.objects.filter(email=self.request.user)
        return query
    

class UserListViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]
    #proteger rotar com autenticacao via token
    #authentication.SessionAuthentication = para que eu tenha acesso a api se estiver autenticado
    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = User.objects.all()
            return queryset
    serializer_class = UserSerializer


class ProfileUserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        queryset = UserProfile.objects.filter(user=self.request.user)
        print(self.request.user.id)
        return queryset
    serializer_class = UserProfileSerializer
