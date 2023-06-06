from django.test.testcases import TestCase

from api.serializers.pedido import PedidoSerializer
from api.tests.factories.item import ItemFactory
from api.tests.factories.pedido import PedidoFactory
from api.tests.factories.user import UserFactory


class PedidoSerializerTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.items = ItemFactory()
        self.data = {
            "user": self.user.pk,
            "items": [{"item": self.items.pk, "quant": 1}],
        }
        self.pedido = PedidoFactory()

    def test_create_pedido(self):
        serializer = PedidoSerializer(data=self.data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        pedido = serializer.save()
        self.assertEqual(pedido.user, self.user)

    def test_serialize_pedido(self):
        data = PedidoSerializer(self.pedido).data
        self.assertEqual(self.pedido.id, data["id"])
