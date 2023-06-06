from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.


class Item(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    preco = models.FloatField(validators=[MinValueValidator(0)])


class Pedido(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="pedidos")


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="pedidos")
    quant = models.IntegerField(validators=[MinValueValidator(0)])
