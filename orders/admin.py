# orders/admin.py

from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['produto'] # Facilita para pedidos grandes
    extra = 0 # Não mostra itens extras por padrão

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'status', 'pagamento_confirmado', 'criado_em']
    list_filter = ['status', 'pagamento_confirmado', 'criado_em']
    search_fields = ['usuario__username', 'id']
    inlines = [OrderItemInline] # Mostra os itens DENTRO do pedido

admin.site.register(Order, OrderAdmin)