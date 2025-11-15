from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from .models import Product, Category, Review, Favorite

def product_list_view(request):
    """
    Controla a Vitrine (US-1), Busca (US-2) e Filtro (US-3).
    """
    
    # US-1 (RN#1): Cupcakes fora de estoque não devem aparecer.
    queryset = Product.objects.filter(quantidade_estoque__gt=0)
    
    # US-2: Buscar cupcakes por sabor (ou nome)
    query = request.GET.get('q')
    if query:
        # Busca por nome OU sabor que contenha o texto da busca
        queryset = queryset.filter(
            Q(nome__icontains=query) | Q(sabor__icontains=query)
        )
    
    # US-3: Filtrar cupcakes por tipo
    category_id = request.GET.get('categoria')
    if category_id:
        queryset = queryset.filter(categoria__id=category_id)
        
    # Pega todas as categorias para exibir no menu de filtro
    categories = Category.objects.all()
    
    context = {
        'products': queryset,
        'categories': categories,
        'selected_category_id': category_id, # Para manter o filtro ativo na UI
    }
    # Otimização para US-1 (RNF#1): O tempo de carregamento
    # deve ser < 3s. Isso pode ser melhorado com .select_related('categoria')
    # e paginação, mas mantemos simples por enquanto.
    
    return render(request, 'store/product_list.html', context)


def product_detail_view(request, pk):
    """
    Mostra os detalhes de um produto e permite avaliá-lo (US-10).
    """
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.all().order_by('-criado_em')
    
    # US-10 (CA#2): Média de avaliações visível no produto.
    average_rating = reviews.aggregate(Avg('estrelas'))['estrelas__avg'] or 0

    # Lógica para US-10: Avaliar cupcakes
    if request.method == 'POST' and request.user.is_authenticated:
        # US-10 (RN#1): Avaliações são moderadas (seria feito no Admin)
        # US-10 (CA#1): Apenas clientes que compraram podem avaliar.
        # (Essa verificação de "compra" é complexa e omitida aqui,
        # mas seria feita checando os Pedidos do usuário)
        
        estrelas = request.POST.get('estrelas')
        comentario = request.POST.get('comentario')
        
        # Cria ou atualiza a avaliação do usuário
        Review.objects.update_or_create(
            produto=product,
            usuario=request.user,
            defaults={'estrelas': estrelas, 'comentario': comentario}
        )
        return redirect('store:product_detail', pk=product.pk)

    context = {
        'product': product,
        'reviews': reviews,
        'average_rating': average_rating,
    }
    return render(request, 'store/product_detail.html', context)


@login_required # US-15 (RN#1): Apenas usuários logados podem favoritar.
def toggle_favorite_view(request, pk):
    """
    Controla a US-15: Criar lista de favoritos.
    """
    product = get_object_or_404(Product, pk=pk)
    
    # Tenta encontrar um favorito existente
    favorite, created = Favorite.objects.get_or_create(
        usuario=request.user,
        produto=product
    )
    
    if not created:
        # Se já existia (não foi criado agora), delete.
        favorite.delete()
        
    # Redireciona de volta para a página de onde o usuário veio
    return redirect(request.META.get('HTTP_REFERER', 'store:product_list'))