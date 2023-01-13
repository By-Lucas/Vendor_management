from django import forms
from accounts.models import User
from accounts.others_models.model_profile import UserProfile, Contact
from helpers import commons


class UserUpdateForm(forms.ModelForm):
    name = forms.CharField(label='Nome completo', required=False,  widget=forms.TextInput(attrs={'class': 'form-control mb-0'}))
    email = forms.EmailField(label='E-mail', required=False,  widget=forms.TextInput(attrs={'class': 'form-control mb-0'}))
    username = forms.CharField(label='Usuário', required=False,  widget=forms.TextInput(attrs={'class': 'form-control mb-0'}))

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
            'house_number', 'pin_code', 'city', 'state', 'email_busines'
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        user = kwargs.pop('user')

        super(UserProfileForm, self).__init__(*args, **kwargs)
        try:
            if user.role == commons.USER_COMMOM:
                self.fields['business_name'] = forms.CharField(widget=forms.HiddenInput(), required=False)
                self.fields['CNPJ'] = forms.CharField(widget=forms.HiddenInput(), required=False)
                self.fields['fantasy_name'] = forms.CharField(widget=forms.HiddenInput(), required=False)
                self.fields['email_busines'] = forms.CharField(widget=forms.HiddenInput(), required=False)
        except AttributeError:
            pass


class ContactForm(forms.ModelForm):
    contact = forms.CharField(label='Contatos', required=False,  widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        modal = Contact
        fields = '__all__'