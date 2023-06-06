import factory
from faker import Faker

from api.models import Item

fake = Faker()


class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Item

    nome = factory.LazyFunction(lambda: fake.name())
    preco = factory.LazyFunction(lambda: fake.pyfloat(min_value=0))
