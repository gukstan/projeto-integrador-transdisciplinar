from django.urls import path
from . import views

# Este 'app_name' ajuda o Django a encontrar as URLs corretas
app_name = 'store'

urlpatterns = [
    # US-1, US-2, US-3: A vitrine principal, com busca e filtro
    path('', views.product_list_view, name='product_list'),
    
    # URL para ver os detalhes de um cupcake específico
    # Também usado para US-10: Avaliar cupcakes
    path('produto/<int:pk>/', views.product_detail_view, name='product_detail'),
    
    # US-15: Ação para adicionar/remover um favorito
    path('produto/<int:pk>/favoritar/', views.toggle_favorite_view, name='toggle_favorite'),
]