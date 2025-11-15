from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # US-8: CPF é obrigatório (RN#1)
    cpf = models.CharField(max_length=14, unique=True, blank=False, null=False)
    
    # US-8: Campos adicionais
    telefone = models.CharField(max_length=15, blank=True)
    endereco = models.TextField(blank=True)
    
    # US-14: Receber promoções por e-mail (CA#1)
    receber_promocoes = models.BooleanField(default=True)

    def __str__(self):
        return self.username