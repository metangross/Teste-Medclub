from django.test.testcases import TestCase

from api.serializers.user import UserSerializer
from api.tests.factories.user import UserFactory


class UserSerializerTest(TestCase):
    def setUp(self):
        self.data = {"username": "teste", "password": "12345"}
        self.user = UserFactory()

    def test_create_user(self):
        serializer = UserSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, serializer.data["username"])

    def test_create_user_repetido(self):
        serializer = UserSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        new_data = {"username": "teste", "password": "123456"}
        new_user = UserSerializer(data=new_data)
        self.assertFalse(new_user.is_valid())

    def test_serialize_user(self):
        data = UserSerializer(self.user).data
        self.assertEqual(self.user.username, data["username"])
