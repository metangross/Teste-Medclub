from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.factories.item import ItemFactory
from api.tests.factories.pedido import ItemPedidoFactory, PedidoFactory
from api.tests.factories.user import UserFactory


class PedidoViewSetTest(APITestCase):
    def setUp(self):
        self.pedido_url = reverse("pedido-view")
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_get_pedido_user(self):
        pedido = PedidoFactory.create_batch(10, user=self.user)
        resp = self.client.get(self.pedido_url)
        self.assertTrue(status.is_success(resp.status_code))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertEqual(len(pedido), len(data))
        for index in range(len(pedido)):
            self.assertEqual(pedido[index].id, data[index]["id"])

    def test_get_item_pedido(self):
        pedido = PedidoFactory(user=self.user)
        item_pedido = ItemPedidoFactory.create_batch(10, pedido=pedido)
        item_pedido_url = reverse("item-pedido-view", kwargs={"pk": pedido.pk})
        resp = self.client.get(item_pedido_url)
        self.assertTrue(status.is_success(resp.status_code))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertEqual(len(item_pedido), len(data))
        for index in range(len(item_pedido)):
            self.assertEqual(item_pedido[index].item.nome, data[index]["item"]["nome"])
            self.assertEqual(
                item_pedido[index].item.preco, data[index]["item"]["preco"]
            )

    def test_get_item_pedido_outro_user(self):
        pedido = PedidoFactory(user=self.user)
        item_pedido_url = reverse("item-pedido-view", kwargs={"pk": pedido.pk})
        new_user = UserFactory()
        self.client.force_authenticate(user=new_user)
        resp = self.client.get(item_pedido_url)
        self.assertTrue(status.is_client_error(resp.status_code))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_pedido(self):
        item = ItemFactory()
        item2 = ItemFactory()
        data = {
            "items": [{"item": item.pk, "quant": 10}, {"item": item2.pk, "quant": 5}]
        }
        resp = self.client.post(self.pedido_url, data, format="json")
        self.assertTrue(status.is_success(resp.status_code))
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.json()
        items = data["items"]
        self.assertEqual(items[0]["item"], item.id)
        self.assertEqual(items[0]["quant"], 10)
        self.assertEqual(items[1]["item"], item2.id)
        self.assertEqual(items[1]["quant"], 5)
