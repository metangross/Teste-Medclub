from rest_framework import status, viewsets
from django.db import transaction
from api.serializers.item import ItemSerializer
from rest_framework.generics import get_object_or_404, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.response import Response
from api.models import Item


class ItemView(RetrieveUpdateDestroyAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()



class ItemListView(ListCreateAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()