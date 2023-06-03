from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from api.models import User, Item, Pedido

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


