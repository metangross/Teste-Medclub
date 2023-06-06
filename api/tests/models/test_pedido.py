from django.test.testcases import TestCase

from api.models import ItemPedido, Pedido
from api.tests.factories.pedido import ItemPedidoFactory, PedidoFactory


class UserTest(TestCase):
    def setUp(self):
        self.pedido = PedidoFactory()
        self.itempedido = ItemPedidoFactory(pedido=self.pedido)

    def test_create_from_factory(self):
        self.assertTrue(isinstance(self.pedido, Pedido))
        self.assertTrue(isinstance(self.itempedido, ItemPedido))
        self.assertEqual(self.itempedido.pedido, self.pedido)
