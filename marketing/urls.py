# marketing/urls.py
from django.urls import path
from . import views

app_name = 'marketing'

urlpatterns = [
    # US-14: Página para ativar/desativar promoções
    path('preferencias-email/', views.subscription_settings_view, name='subscription_settings'),
]