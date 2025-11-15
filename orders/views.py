# orders/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Order, OrderItem
from store.models import Product
import decimal # Para lidar com os valores

# --- Funções do Carrinho (US-4) ---

def add_to_cart_view(request, product_id):
    """
    Controla US-4: Adicionar cupcake ao carrinho.
    Usa a sessão do Django para armazenar o carrinho.
    """
    product = get_object_or_404(Product, id=product_id)
    
    # Inicializa o carrinho na sessão se não existir
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    # Pega a quantidade atual no carrinho, ou 0
    current_quantity = cart.get(product_id_str, 0)
    
    # US-4 (RN#1): Quantidade máxima por pedido: 50 unidades (aqui consideramos por *item*)
    if current_quantity >= 50:
        messages.error(request, 'Quantidade máxima de 50 unidades por item atingida.')
    else:
        cart[product_id_str] = current_quantity + 1
        messages.success(request, f'"{product.nome}" foi adicionado ao carrinho.')

    request.session['cart'] = cart
    return redirect('orders:cart_detail')

def remove_from_cart_view(request, product_id):
    """
    Remove um item do carrinho ou diminui a quantidade.
    """
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        cart[product_id_str] -= 1
        if cart[product_id_str] <= 0:
            del cart[product_id_str] # Remove o item se a quantidade for 0
    
    request.session['cart'] = cart
    return redirect('orders:cart_detail')

def cart_detail_view(request):
    """
    Mostra a página do carrinho (US-4).
    """
    cart = request.session.get('cart', {})
    cart_items = []
    subtotal = decimal.Decimal(0)

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total_item = product.valor * quantity
        subtotal += total_item
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_item': total_item,
        })
        
    # US-5 (RN#1): Pedido mínimo de R$ 10,00.
    min_order_met = subtotal >= decimal.Decimal(10.00)
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'min_order_met': min_order_met,
    }
    return render(request, 'orders/cart_detail.html', context)


# --- Funções de Checkout (US-5, US-6, US-13) ---

def calculate_shipping_view(request):
    """
    Controla US-13: Calcular frete por CEP (Simulação)
    """
    cep = request.GET.get('cep')
    if not cep:
        return JsonResponse({'error': 'CEP não fornecido'}, status=400)

    # --- INÍCIO DA INTEGRAÇÃO COM API (Ex: Correios) ---
    # Aqui você chamaria a API dos Correios com o 'cep'.
    # Para simular:
    try:
        # Simula uma regra de frete
        if cep.startswith('0'): 
            valor_frete = decimal.Decimal(5.00)
            prazo = "2 dias úteis"
        else:
            valor_frete = decimal.Decimal(10.00)
            prazo = "5 dias úteis"
            
        # US-13 (RN#1): Frete grátis acima de R$100 (seria verificado no checkout)
        
        return JsonResponse({
            'valor': valor_frete, # CA#1
            'prazo': prazo,     # CA#1
        })
    except Exception as e:
        return JsonResponse({'error': 'Não foi possível calcular o frete.'}, status=500)
    # --- FIM DA INTEGRAÇÃO COM API ---

@login_required # Usuário deve estar logado para finalizar o pedido
def checkout_view(request):
    """
    Controla US-5: Finalizar pedido.
    """
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'Seu carrinho está vazio.')
        return redirect('store:product_list')

    # Pega o subtotal (calculado novamente para segurança)
    subtotal = decimal.Decimal(0)
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal += product.valor * quantity
        
    # US-5 (RN#1): Pedido mínimo de R$ 10,00
    if subtotal < decimal.Decimal(10.00):
        messages.error(request, 'Seu pedido deve ter um valor mínimo de R$ 10,00.')
        return redirect('orders:cart_detail')
        
    # Lógica de frete (simplificada)
    frete = decimal.Decimal(10.00) # Valor fixo por simplicidade
    
    # US-13 (RN#1): Frete grátis
    if subtotal >= decimal.Decimal(100.00):
        frete = decimal.Decimal(0.00)
        
    valor_total = subtotal + frete
    
    # Processa a criação do pedido
    if request.method == 'POST':
        # --- INÍCIO DA INTEGRAÇÃO DE PAGAMENTO (US-6) ---
        # Aqui você integraria com o PIX (ex: Mercado Pago).
        # Se o pagamento for confirmado:
        payment_confirmed = True # Simulando pagamento aprovado
        # --- FIM DA INTEGRAÇÃO DE PAGAMENTO ---

        if payment_confirmed:
            # US-6 (RN#1): Pedido só é liberado após pagamento.
            order = Order.objects.create(
                usuario=request.user,
                valor_total=valor_total,
                valor_frete=frete,
                status='recebido', # US-7: Status inicial
                pagamento_confirmado=True
            )
            # Adiciona os itens do carrinho ao pedido
            for product_id, quantity in cart.items():
                product = get_object_or_404(Product, id=product_id)
                OrderItem.objects.create(
                    pedido=order,
                    produto=product,
                    quantidade=quantity,
                    valor_unitario=product.valor
                )
                # Abater do estoque (US-11)
                product.quantidade_estoque -= quantity
                product.save()
            
            # Limpa o carrinho da sessão
            del request.session['cart']
            
            messages.success(request, 'Pedido realizado com sucesso!')
            return redirect('orders:order_detail', pk=order.pk)
        else:
            messages.error(request, 'Pagamento falhou.')
            
    context = {
        'subtotal': subtotal,
        'frete': frete,
        'valor_total': valor_total,
    }
    return render(request, 'orders/checkout.html', context)


# --- Funções de Status do Pedido (US-7) ---

@login_required
def order_list_view(request):
    """
    Mostra a lista de pedidos do usuário (US-7).
    """
    orders = Order.objects.filter(usuario=request.user).order_by('-criado_em')
    context = {'orders': orders}
    return render(request, 'orders/order_list.html', context)

@login_required
def order_detail_view(request, pk):
    """
    Mostra os detalhes e o status de um pedido específico (US-7).
    """
    order = get_object_or_404(Order, pk=pk, usuario=request.user)
    context = {'order': order}
    return render(request, 'orders/order_detail.html', context)