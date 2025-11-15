from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # Adicione os campos do seu CustomUser aqui
        # US-8: CPF é obrigatório (RN#1)
        fields = ('username', 'email', 'cpf', 'telefone', 'endereco', 'receber_promocoes')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'cpf', 'telefone', 'endereco', 'receber_promocoes')