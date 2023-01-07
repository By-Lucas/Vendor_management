from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from helpers.managers import UserManager
from helpers.commons import BASE_ACCESS_LEVEL_CHOICES


class User(AbstractBaseUser):
    username_validator = UnicodeUsernameValidator()

    name = models.CharField(verbose_name=_('Nome'), max_length=150, help_text=_('Informe seu nome completo'))
    email = models.EmailField(verbose_name=_('E-mail'), unique=True,
                              help_text=_('Seu melhor e-mail. Será usado para login também.'))
    username = models.CharField(_('Usuário'),max_length=150,unique=True,validators=[username_validator],
                                    help_text=_('Obrigatório. 150 caracteres ou menos. Letras, números e os símbolos @/./+/-/_ são permitidos.'),
                                    error_messages={'unique': _("Já existe um usuário com este username."),}
                                )
    is_staff = models.BooleanField(verbose_name=_('Staff'), default=False, help_text=_('Pode logar no Admin'))
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(verbose_name=_('Usuário administrador'),default=False, help_text=_('Usuário com acesso irrestrito no sistema.'))
    is_active = models.BooleanField(verbose_name=_("Ativo"),default=False, help_text=_('Desmarque esta opção em vez de deletar o usuário.'))
    date_joined = models.DateTimeField(verbose_name=_('Data de cadastro'), default=timezone.now, editable=False)
    user_clipse = models.BooleanField(verbose_name=_('Usuário Clipse'), default=False, help_text=_('Usuário com acesso irrestrito no sistema.'))
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    role = models.CharField(verbose_name=_("Tipo de usuário"), choices=BASE_ACCESS_LEVEL_CHOICES, blank=True, null=True, max_length=100)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('Usuário')
        verbose_name_plural = _('Usuários')

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True