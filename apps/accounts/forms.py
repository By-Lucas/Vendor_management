from django import forms

from accounts.models import User
from accounts.others_models.model_profile import UserProfile, Contact
from helpers import commons


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'name',
            'email',
            'username',
        ]


class UserForm(forms.ModelForm):
    password = forms.CharField(label='Senha', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirme sua senha', widget=forms.PasswordInput())
    role = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'role', 'password', 'confirm_password']

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
            'profile_picture', 'business_name',
            'CNPJ', 'fantasy_name', 'address', 'complement_address', 'district',
            'house_number', 'pin_code', 'city', 'state', 'phone', 'email_busines'
        ]

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        self.request = kwargs.pop('request', None)
        user = kwargs.pop('instance')

        try:
        
            if user.role == commons.USER_COMMOM:
                self.fields['business_name'] = forms.CharField(widget=forms.HiddenInput())
                self.fields['CNPJ'] = forms.CharField(widget=forms.HiddenInput())
                self.fields['fantasy_name'] = forms.CharField(widget=forms.HiddenInput())
                self.fields['email_busines'] = forms.CharField(widget=forms.HiddenInput())
        except AttributeError:
            pass


class ContactForm(forms.ModelForm):
    class Meta:
        modal = Contact
        fields = ['contact']