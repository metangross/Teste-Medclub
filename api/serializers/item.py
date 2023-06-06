from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from api.models import Item, Pedido, User


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class ItemSerializerOutput(ItemSerializer):
    class Meta:
        model = Item
        exclude = ["id"]
