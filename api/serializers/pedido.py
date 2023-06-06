from django.contrib.auth.models import User
from django.db import transaction
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from api.models import Item, ItemPedido, Pedido
from api.serializers.item import ItemSerializerOutput


class ItensSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPedido
        fields = ["item", "quant"]


class ItensSerializerDetalhado(serializers.ModelSerializer):
    item = ItemSerializerOutput()

    class Meta:
        model = ItemPedido
        fields = ["item", "quant"]


class PedidoSerializer(WritableNestedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )
    items = ItensSerializer(many=True)

    class Meta:
        model = Pedido
        fields = "__all__"

    @transaction.atomic
    def create(self, validated_data):
        return super().create(validated_data)


class PedidoSerializerOutput(WritableNestedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )

    class Meta:
        model = Pedido
        fields = "__all__"
