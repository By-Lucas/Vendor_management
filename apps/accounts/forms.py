from django import forms

from accounts.models import User
from accounts.others_models.model_profile import UserProfile
from helpers.commons import ADMIN_SISTEM, BASE_ACCESS_LEVEL_CHOICES


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'name',
            'email',
            'username',
            'role',
        ]


class UserForm(forms.ModelForm):
    password = forms.CharField(label='Senha', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirme sua senha', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Senha não corresponde!")


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'profile_picture', 'cover_photo', 'business_name',
            'CNPJ', 'fantasy_name', 'address', 'complement_address', 'district',
            'house_number', 'pin_code', 'city', 'state', 'phone', 'email_busines'
        ]
