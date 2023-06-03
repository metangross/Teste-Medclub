from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.

class User (models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=240)

class Item (models.Model):
    nome = models.CharField(max_length=100, unique=True)
    preco = models.FloatField(validators=[MinValueValidator(0)])

class Pedido (models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name="pedidos")
    