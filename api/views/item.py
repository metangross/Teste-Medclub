from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from api.models import Item
from api.serializers.item import ItemSerializer


class ItemView(RetrieveUpdateDestroyAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()


class ItemListView(ListCreateAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
