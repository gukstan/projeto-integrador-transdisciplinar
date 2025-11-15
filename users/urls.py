from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    # US-8: Cadastro de cliente
    path('cadastro/', views.register_view, name='register'),
    
    # US-9: Login do cliente
    # Usamos a view pronta do Django para login
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html'
    ), name='login'),
    
    # View de Logout
    path('logout/', auth_views.LogoutView.as_view(
        next_page='store:product_list' # Para onde vai após o logout
    ), name='logout'),
]