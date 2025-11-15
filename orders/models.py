from django.db import models
from django.conf import settings
from store.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('recebido', 'Recebido'),
        ('em_preparo', 'Em Preparo'),
        ('saiu_para_entrega', 'Saiu para Entrega'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]
    
    TIPO_ENTREGA_CHOICES = [
        ('entrega', 'Entrega'),
        ('retirada', 'Retirada'),
    ]

    # US-5: Cliente e info do pedido
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    tipo_entrega = models.CharField(max_length=10, choices=TIPO_ENTREGA_CHOICES, default='entrega')
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # US-13: Cálculo de frete
    valor_frete = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
    # US-7: Acompanhar status (Ação)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='recebido')
    
    # US-6: Pagamento via Pix
    pagamento_confirmado = models.BooleanField(default=False)
    
    criado_em = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Pedido #{self.id} - {self.usuario.username}'

class OrderItem(models.Model):
    # US-4: Item do carrinho (que vira item do pedido)
    pedido = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    produto = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantidade = models.PositiveIntegerField(default=1)
    
    # US-4 (CA#1): Valor total do item
    valor_unitario = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome}'