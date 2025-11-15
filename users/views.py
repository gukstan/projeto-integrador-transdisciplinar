from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm

def register_view(request):
    """
    Controla o US-8: Cadastro de cliente.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redireciona para a página de login após o cadastro
            return redirect('users:login') 
    else:
        form = CustomUserCreationForm()
        
    context = {
        'form': form
    }
    return render(request, 'users/register.html', context)

# Observação: A view de Login (US-9) é tratada
# diretamente no urls.py, usando a LoginView do Django.
# Não precisamos de uma view para ela aqui,
# a menos que precisemos de lógica extra.

# US-9 (RN#1): "Após 5 tentativas erradas, a conta é bloqueada"
# Isso é uma configuração avançada. Recomendo usar um pacote
# como `django-axes` para implementar isso de forma segura.

# US-9 (RNF#1): "Sessão expira após 15 minutos"
# Isso é configurado no 'settings.py', não aqui.
# Adicione: SESSION_COOKIE_AGE = 900 (900 segundos = 15 minutos)