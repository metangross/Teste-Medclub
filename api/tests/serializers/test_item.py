from django.test.testcases import TestCase

from api.serializers.item import ItemSerializer
from api.tests.factories.item import ItemFactory


class ItemSerializerTest(TestCase):
    def setUp(self):
        self.data = {"nome": "item teste", "preco": 10}
        self.item = ItemFactory()

    def test_create_item(self):
        serializer = ItemSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        item = serializer.save()
        self.assertEqual(item.nome, serializer.data["nome"])
        self.assertEqual(item.preco, serializer.data["preco"])

    def test_create_nome_invalido(self):
        serializer = ItemSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        new_data = {"nome": "item teste", "preco": 150}
        new_item = ItemSerializer(data=new_data)
        self.assertFalse(new_item.is_valid())

    def test_create_valor_invalido(self):
        self.data["preco"] = -10
        serializer = ItemSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

    def test_serialize_item(self):
        data = ItemSerializer(self.item).data
        self.assertEqual(self.item.nome, data["nome"])
        self.assertEqual(self.item.preco, data["preco"])
