from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from api.models import User, Item, Pedido, ItemPedido

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = "__all__"

class ItensSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPedido
        fields = [
            "item",
            "quant"
        ]

class ItemPedidoSerializer(serializers.Serializer):
    user = PedidoSerializer()
    items = ItensSerializer(many=True)
    
        
