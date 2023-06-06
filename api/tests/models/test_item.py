from django.test.testcases import TestCase

from api.models import Item
from api.tests.factories.item import ItemFactory


class ItemTest(TestCase):
    def setUp(self):
        self.item = ItemFactory()

    def test_create_from_factory(self):
        self.assertTrue(isinstance(self.item, Item))
