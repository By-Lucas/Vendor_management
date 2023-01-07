from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User
from accounts.others_models.model_profile import UserProfile

class CustomUserAdmin(UserAdmin):
    list_display = ['name', 'email', 'is_superuser', 'is_staff', 'role']
    list_filter = []
    search_fields = ['name', 'email']
    filter_horizontal = []
    fieldsets = (
        (None, {'fields': ('name', 'email', 'username', 'password', 'role')}),
        ('Permissão', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin')}),
    )
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': (
        'name', 'role',
        'username', 'email',
        'password1', 'password2',
    )}),)


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)
