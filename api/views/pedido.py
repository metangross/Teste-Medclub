from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response

from api.models import Pedido
from api.serializers.pedido import (
    ItensSerializerDetalhado,
    PedidoSerializer,
    PedidoSerializerOutput,
)


class PedidoView(ListCreateAPIView):
    serializer_class = PedidoSerializer
    queryset = Pedido.objects.all()

    def get(self, request, *args, **kwargs):
        user = request.user
        pedidos = Pedido.objects.filter(user=user)
        data = PedidoSerializerOutput(instance=pedidos, many=True)
        return Response(data=data.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        request.data.update({"user": user.pk})
        return super().post(request, *args, **kwargs)


class PedidoUserView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        pk = kwargs["pk"]
        pedido = Pedido.objects.get(id=pk)
        if user.pk != pedido.user.pk:
            return Response(
                data={"detail": "Sem autorização para acessar o pedido"},
                status=status.HTTP_403_FORBIDDEN,
            )
        data = ItensSerializerDetalhado(instance=pedido.items.all(), many=True)
        return Response(data=data.data, status=status.HTTP_200_OK)
