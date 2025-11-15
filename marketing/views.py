# marketing/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required # O usuário precisa estar logado para mudar suas preferências
def subscription_settings_view(request):
    """
    Controla US-14: Permite ao cliente ativar/desativar
    o recebimento de promoções por e-mail.
    """
    
    # Pega o usuário da requisição
    user = request.user

    if request.method == 'POST':
        # Lógica para ATUALIZAR a preferência
        
        # Um checkbox HTML envia 'on' se marcado, e não envia nada se desmarcado.
        # Então, verificamos se 'receber_promocoes' está no request.POST
        new_status = 'receber_promocoes' in request.POST
        
        user.receber_promocoes = new_status
        user.save()
        
        messages.success(request, 'Suas preferências de comunicação foram atualizadas.')
        return redirect('marketing:subscription_settings')

    # Lógica para EXIBIR a página
    context = {
        'receber_promocoes': user.receber_promocoes
    }
    return render(request, 'marketing/subscription_settings.html', context)