# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Mostra seus campos personalizados (CPF, etc.) no admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Campos que aparecem na lista de usuários
    list_display = ['username', 'email', 'cpf', 'is_staff']
    # Campos que aparecem ao editar o usuário
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('cpf', 'telefone', 'endereco', 'receber_promocoes')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('cpf', 'telefone', 'endereco', 'receber_promocoes')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)