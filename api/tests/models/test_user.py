from django.contrib.auth.models import User
from django.test.testcases import TestCase

from api.tests.factories.user import UserFactory


class UserTest(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_create_from_factory(self):
        self.assertTrue(isinstance(self.user, User))
