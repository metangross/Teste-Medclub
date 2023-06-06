import factory
from faker import Faker

from api.models import ItemPedido, Pedido
from api.tests.factories.item import ItemFactory
from api.tests.factories.user import UserFactory

fake = Faker()


class PedidoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Pedido

    user = factory.SubFactory(UserFactory)


class ItemPedidoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ItemPedido

    pedido = factory.SubFactory(PedidoFactory)
    item = factory.SubFactory(ItemFactory)
    quant = factory.LazyFunction(lambda: fake.pyint(min_value=0))
