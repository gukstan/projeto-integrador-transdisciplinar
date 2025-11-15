# orders/urls.py
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # US-4: Adicionar cupcake ao carrinho (e ver o carrinho)
    path('carrinho/', views.cart_detail_view, name='cart_detail'),
    path('carrinho/adicionar/<int:product_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('carrinho/remover/<int:product_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    
    # US-13: Endpoint (simulado) para calcular frete
    path('carrinho/calcular-frete/', views.calculate_shipping_view, name='calculate_shipping'),

    # US-5: Finalizar pedido
    path('finalizar-pedido/', views.checkout_view, name='checkout'),
    
    # US-7: Acompanhar status do pedido
    path('meus-pedidos/', views.order_list_view, name='order_list'),
    path('meus-pedidos/<int:pk>/', views.order_detail_view, name='order_detail'),
]