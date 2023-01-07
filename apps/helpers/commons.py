from django.utils.translation import gettext_lazy as _

ADMIN_SISTEM = 'adm_sistem_access'
USER_COMMOM = 'user_commom_access'
VENDOR = 'user_suppliers_access'

BASE_ACCESS_LEVEL_CHOICES = (
    (ADMIN_SISTEM, _('Administrador sistema')),
    (VENDOR, _('Fornecedor')),
    (USER_COMMOM, _('Usuário')),
)
