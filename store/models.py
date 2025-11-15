from django.db import models
from django.conf import settings

# US-3: Para filtrar cupcakes por tipo
class Category(models.Model):
    TIPO_CHOICES = [
        ('doce', 'Doce'),
        ('salgado', 'Salgado'),
        ('diet', 'Diet'),
    ]
    nome = models.CharField(max_length=50, choices=TIPO_CHOICES)

    def __str__(self):
        return self.get_nome_display()

class Product(models.Model):
    # US-1: Campos do cupcake (CA#2)
    nome = models.CharField(max_length=100)
    sabor = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='cupcakes/')
    valor = models.DecimalField(max_digits=6, decimal_places=2)
    
    # US-11: Gerenciar estoque (CA#1)
    quantidade_estoque = models.PositiveIntegerField(default=0)
    
    # US-3: Relação com Categoria
    categoria = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    @property
    def em_estoque(self):
        # US-1 (RN#1): Cupcakes fora de estoque não devem aparecer.
        return self.quantidade_estoque > 0

    def __str__(self):
        return self.nome

# US-10: Avaliar cupcakes
class Review(models.Model):
    produto = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # US-10: Sistema de estrelas (1-5) e comentário
    estrelas = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comentario = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('produto', 'usuario') # Um review por usuário/produto

# US-15: Criar lista de favoritos
class Favorite(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    produto = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by')
    
    class Meta:
        unique_together = ('usuario', 'produto') # Um favorito por usuário/produto

    def __str__(self):
        return f'{self.usuario.username} favoritou {self.produto.nome}'