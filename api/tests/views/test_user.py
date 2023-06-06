import copy

from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.factories.user import UserFactory


class UserViewSetTest(APITestCase):
    def setUp(self):
        self.user_url = reverse("user-view")
        self.data = {"username": "teste", "password": "teste"}

    def test_get_user(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        resp = self.client.get(self.user_url)
        self.assertTrue(status.is_success(resp.status_code))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertEqual(user.username, data["username"])
        self.assertEqual(user.id, data["id"])
        self.assertEqual(user.last_login, data["last_login"])
        self.assertEqual(user.is_superuser, data["is_superuser"])
        self.assertEqual(user.first_name, data["first_name"])
        self.assertEqual(user.last_name, data["last_name"])
        self.assertEqual(user.email, data["email"])
        self.assertEqual(user.is_staff, data["is_staff"])
        self.assertEqual(user.is_active, data["is_active"])

    def test_post_user(self):
        user_post_url = reverse("user-list-view")
        resp = self.client.post(user_post_url, self.data, format="json")
        self.assertTrue(status.is_success(resp.status_code))
        self.assertEqual(status.HTTP_201_CREATED, resp.status_code)
        data = resp.json()
        self.assertEqual(self.data["username"], data["username"])

    def test_post_user_repetido(self):
        user_post_url = reverse("user-list-view")
        resp = self.client.post(user_post_url, self.data, format="json")
        self.assertTrue(status.is_success(resp.status_code))
        self.assertEqual(status.HTTP_201_CREATED, resp.status_code)
        resp = self.client.post(user_post_url, self.data, format="json")
        self.assertTrue(status.is_client_error(resp.status_code))
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_user(self):
        user = UserFactory(username="teste", password="12345")
        user_copy = copy.deepcopy(user)
        patch = {"username": "novoteste"}
        self.client.force_authenticate(user=user)
        resp = self.client.patch(self.user_url, data=patch, format="json")
        self.assertTrue(status.is_success(resp.status_code))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertNotEqual(user_copy.username, data["username"])
        self.assertEqual(user.username, data["username"])

    def test_auth_user(self):
        user = UserFactory(
            username=self.data["username"],
            password=make_password(self.data["password"]),
        )
        user_auth_url = reverse("login-view")
        resp = self.client.post(user_auth_url, self.data, format="json")
        self.assertTrue(status.is_success(resp.status_code))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertEqual("Login realizado com sucesso.", data["message"])

    def test_user_no_auth(self):
        self.client.logout()
        resp = self.client.get(self.user_url)
        self.assertTrue(status.is_client_error(resp.status_code))
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        patch = {"username": "novoteste"}
        resp = self.client.patch(self.user_url, data=patch, format="json")
        self.assertTrue(status.is_client_error(resp.status_code))
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
