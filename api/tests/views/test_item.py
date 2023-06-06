from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Item
from api.tests.factories.item import ItemFactory


class ItemViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username="teste", password="12345")
        self.item_list_url = reverse("item-list-view")
        self.data = {"nome": "item teste", "preco": 10}
        self.client.force_authenticate(user=self.user)

    def test_get_item(self):
        item = ItemFactory()
        item_detail_url = reverse("item-view", kwargs={"pk": item.pk})
        resp = self.client.get(item_detail_url)
        self.assertTrue(status.is_success(resp.status_code))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertEqual(item.nome, data["nome"])
        self.assertEqual(item.preco, data["preco"])

    def test_get_item_list(self):
        item = ItemFactory.create_batch(10)
        resp = self.client.get(self.item_list_url)
        self.assertTrue(status.is_success(resp.status_code))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertEqual(len(item), len(data))
        for index in range(len(item)):
            self.assertEqual(item[index].nome, data[index]["nome"])
            self.assertEqual(item[index].preco, data[index]["preco"])

    def test_post_item(self):
        resp = self.client.post(self.item_list_url, self.data, format="json")
        self.assertTrue(status.is_success(resp.status_code))
        self.assertEqual(status.HTTP_201_CREATED, resp.status_code)
        data = resp.json()
        self.assertEqual(self.data["nome"], data["nome"])
        self.assertEqual(self.data["preco"], data["preco"])
        self.assertEqual(Item.objects.count(), 1)

    def test_post_item_preco_invalido(self):
        data = {"nome": "item teste", "preco": -10}
        resp = self.client.post(self.item_list_url, data, format="json")
        self.assertTrue(status.is_client_error(resp.status_code))
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_item_nome_igual(self):
        resp = self.client.post(self.item_list_url, self.data, format="json")
        self.assertTrue(status.is_success(resp.status_code))
        self.assertEqual(status.HTTP_201_CREATED, resp.status_code)
        resp = self.client.post(self.item_list_url, self.data, format="json")
        self.assertTrue(status.is_client_error(resp.status_code))
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_item(self):
        item = ItemFactory(nome="teste", preco=35.1)
        patch = {"nome": "novoteste", "preco": 11.1}
        item_patch_url = reverse("item-view", kwargs={"pk": item.pk})
        resp = self.client.patch(item_patch_url, data=patch, format="json")
        self.assertTrue(status.is_success(resp.status_code))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertNotEqual(item.nome, data["nome"])
        self.assertNotEqual(item.preco, data["preco"])

    def test_patch_item_preco_invalido(self):
        item = ItemFactory(nome="teste", preco=35.1)
        patch = {"nome": "novoteste", "preco": -11.1}
        item_patch_url = reverse("item-view", kwargs={"pk": item.pk})
        resp = self.client.patch(item_patch_url, data=patch, format="json")
        self.assertTrue(status.is_client_error(resp.status_code))
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_item_nome_igual(self):
        item = ItemFactory(nome="teste", preco=35.1)
        item = ItemFactory(nome="novoteste", preco=35.1)
        patch = {"nome": "teste", "preco": -11.1}
        item_patch_url = reverse("item-view", kwargs={"pk": item.pk})
        resp = self.client.patch(item_patch_url, data=patch, format="json")
        self.assertTrue(status.is_client_error(resp.status_code))
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
