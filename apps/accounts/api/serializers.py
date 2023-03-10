from rest_framework import serializers

from accounts.others_models.model_profile import UserProfile
from accounts.models import User




class UserSerializer(serializers.HyperlinkedModelSerializer):
    
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        label="Senha"
    )

    password_confirm = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        label="Confirme a senha"
    )

    is_staff = serializers.BooleanField(
        label="Membro da Equipe",
        help_text="Indica que usuário consegue acessar o site de administração."
    )

    is_superuser = serializers.BooleanField(
        label="SuperUsuário",
        help_text="Indica que este usuário tem todas as permissões sem atribuí-las explicitamente."
    )

    class Meta:
        model = User
        fields = ('name', 'username','email','role', 'password', 'password_confirm', 'is_staff', 'is_superuser')
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        count = User(
            email=self.validated_data['email'], 
            username=self.validated_data['username'],
            is_staff=self.validated_data['is_staff'],
            is_superuser=self.validated_data['is_superuser']
        )
        password = self.validated_data['password']
        password_confirm = self.validated_data['password_confirm']

        if password != password_confirm:
            raise serializers.ValidationError({'password': 'As senhas não são iguais.'})
        count.set_password(password)
        count.save()
        return count


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserProfile
        fields = [
            'user', 'profile_picture', 'business_name',
            'CNPJ', 'fantasy_name', 'address', 'complement_address', 'district',
            'house_number', 'pin_code', 'city', 'state', 'email_busines'
        ]