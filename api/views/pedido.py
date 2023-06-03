from rest_framework import status, viewsets
from django.db import transaction
from api.serializers.pedido import ItemPedidoSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from api.models import Item, Pedido

class PedidoView(ListCreateAPIView):
    serializer_class = ItemPedidoSerializer
    queryset = Item.objects.all()
