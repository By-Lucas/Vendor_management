from django.db import models
from django.db.models import Sum
from django.db.models.fields.related import OneToOneField
from django.utils.translation import gettext_lazy as _
from localflavor.br.br_states import STATE_CHOICES

from accounts.models import User


def upload_to(instance, filename):
    return 'users/{username}/{filename}'.format(
        username=instance.user.username, filename=filename)


class UserProfile(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    profile_picture = models.ImageField(upload_to=upload_to, blank=True, null=True)
    cover_photo = models.ImageField(upload_to=upload_to, blank=True, null=True)
    business_name = models.CharField(verbose_name=_('Razão Social'), max_length=100, blank=True, null=True)
    CNPJ = models.CharField(verbose_name=_('CNPJ'), max_length=18, blank=True, null=True)
    fantasy_name = models.CharField(verbose_name=_('Nome Fantasia'), max_length=100, blank=True, null=True)
    address = models.CharField(verbose_name=_('Endereço'), max_length=120, blank=True, null=True)
    complement_address = models.CharField(verbose_name=_('Complemento'), max_length=120, blank=True, null=True)
    district = models.CharField(verbose_name=_('Bairro'), max_length=120, blank=True, null=True)
    house_number = models.PositiveIntegerField(verbose_name=_('Número'), blank=True, null=True)
    pin_code = models.CharField(verbose_name=_('CEP'), max_length=20, blank=True, null=True, help_text='Exemplo: 64800-000')
    city = models.CharField(verbose_name=_('Cidade'), max_length=50, blank=True, null=True)
    state = models.CharField(verbose_name=_('Estado'), max_length=50, choices=STATE_CHOICES, blank=True, null=True)
    phone = models.CharField(verbose_name=_('Telefone'), max_length=120, blank=True, null=True)
    email_busines = models.CharField(verbose_name=_('E-mail'), max_length=120, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = _('Perfil do usuário')
        verbose_name_plural = _('Perfil dos usuários')

    def get_cnpj(self):
        if self.CNPJ:
            cpf = str(self.CNPJ)
            cpf_parte_1 = cpf[0:3]
            cpf_parte_2 = cpf[3:6]
            cpf_parte_3 = cpf[6:9]
            cpf_parte_4 = cpf[9:]
            cpf_formatado = f"{cpf_parte_1}.{cpf_parte_2}.{cpf_parte_3}-{cpf_parte_4}"
            return cpf_formatado
