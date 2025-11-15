# dashboard/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum, Count
from store.models import Product
from orders.models import Order, OrderItem
from django.utils import timezone
from datetime import timedelta

# --- Decorator de Segurança ---
# Garante que apenas administradores (staff) acessem o dashboard
def is_admin(user):
    return user.is_authenticated and user.is_staff

# --- Views do Dashboard ---

@user_passes_test(is_admin)
def dashboard_index_view(request):
    """
    Página inicial do dashboard com links para as seções.
    """
    # Exemplo de dados rápidos:
    total_pedidos_hoje = Order.objects.filter(
        criado_em__gte=timezone.now().replace(hour=0, minute=0, second=0)
    ).count()
    
    context = {
        'total_pedidos_hoje': total_pedidos_hoje,
    }
    return render(request, 'dashboard/index.html', context)

# --- US-11: Gerenciar Estoque ---

@user_passes_test(is_admin)
def manage_stock_view(request):
    """
    Controla US-11: Listar produtos para gerenciar estoque.
    """
    products = Product.objects.all().order_by('nome')
    context = {'products': products}
    return render(request, 'dashboard/manage_stock.html', context)

@user_passes_test(is_admin)
def update_stock_view(request, pk):
    """
    Controla US-11: Editar (cadastrar/remover seriam similares)
    Esta view atualiza a quantidade de estoque de um produto.
    """
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        try:
            # Pega a nova quantidade do formulário
            nova_quantidade = int(request.POST.get('quantidade_estoque'))
            if nova_quantidade < 0:
                raise ValueError()

            product.quantidade_estoque = nova_quantidade
            product.save()
            
            # US-11 (CA#1): "Ao atingir estoque zero, o produto é ocultado da vitrine."
            # Isso já é tratado automaticamente pelo `Product.em_estoque`
            # que criamos no `store/models.py`.

            return redirect('dashboard:manage_stock')
            
        except (ValueError, TypeError):
            # Lida com entrada inválida (ex: "abc" ou "-5")
            context = {'product': product, 'error': 'Por favor, insira um número válido.'}
            return render(request, 'dashboard/update_stock.html', context)

    context = {'product': product}
    return render(request, 'dashboard/update_stock.html', context)

# --- US-12: Relatórios de Vendas ---

@user_passes_test(is_admin)
def sales_report_view(request):
    """
    Controla US-12: Gerar relatórios de vendas.
    """
    # Filtros (US-12)
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    # Filtra pedidos confirmados
    orders = Order.objects.filter(pagamento_confirmado=True)

    if date_from:
        orders = orders.filter(criado_em__gte=date_from)
    if date_to:
        # Adiciona 1 dia ao 'date_to' para incluir o dia inteiro
        date_to_inclusive = timezone.datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1)
        orders = orders.filter(criado_em__lt=date_to_inclusive)

    # US-12 (CA#1): Total vendido (valor)
    total_vendido = orders.aggregate(Sum('valor_total'))['valor_total__sum'] or 0
    
    # US-12 (CA#1): Produtos mais vendidos
    # (Filtra por 'order__in=orders' para usar os filtros de data)
    produtos_mais_vendidos = OrderItem.objects.filter(pedido__in=orders) \
        .values('produto__nome') \
        .annotate(total_unidades=Sum('quantidade')) \
        .order_by('-total_unidades')[:10] # Top 10

    # US-12 (CA#2): Filtro por categorias (seria similar aos filtros de data)
    
    context = {
        'orders': orders,
        'total_vendido': total_vendido,
        'produtos_mais_vendidos': produtos_mais_vendidos,
        'date_from': date_from,
        'date_to': date_to,
    }
    
    # US-12 (RNF#1): Relatórios gerados em até 5 segundos.
    # (Se ficar lento, esta consulta precisaria ser otimizada ou cacheada)
    
    return render(request, 'dashboard/sales_report.html', context)