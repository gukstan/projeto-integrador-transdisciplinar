# dashboard/urls.py
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Página inicial do dashboard
    path('', views.dashboard_index_view, name='index'),

    # US-11: Gerenciar estoque de cupcakes
    path('estoque/', views.manage_stock_view, name='manage_stock'),
    path('estoque/editar/<int:pk>/', views.update_stock_view, name='update_stock'),

    # US-12: Gerar relatórios de vendas
    path('relatorios/vendas/', views.sales_report_view, name='sales_report'),
]