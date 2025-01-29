from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='john', password='<PASSWORD>',
                                            age=26)
        cls.user2 = User.objects.create_user(username='bob', password='<PASSWORD>',
                                             age=26)

    def get_incorrect_user_data(self):
        return {
            "username": "johnny",
            "password": "<PASSWORD>",
            "age": "8"
        }

    def get_new_user_data(self):
        return {
            "username": "johnny",
            "password": "<PASSWORD>",
            "age": "25"
        }

    def get_user_data(self):
        return {
            "username": 'john',
            "password": '<PASSWORD>',
            "age": 26,
        }

    def get_user2_data(self):
        return {
            "username": 'bob',
            "password": '<PASSWORD>',
            "age": 26,
        }


class TestUser(UserAPITestCase):
    url = reverse_lazy('user-list')

    def test_create(self):
        count = User.objects.count()
        response = self.client.post(self.url, data=self.get_user_data())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(self.url, data=self.get_incorrect_user_data())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(self.url, data=self.get_new_user_data())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve(self):
        response = self.client.get(self.url + '%d/' % self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        response = self.client.put(self.url + '%d/' % self.user.pk,
                                   data=self.get_user2_data())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.url + '%d/' % self.user.pk,
                                   data=self.get_incorrect_user_data())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.url + '%d/' % self.user.pk,
                                   data=self.get_user_data())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        count = User.objects.count()
        response = self.client.delete(self.url + '%d/' % self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), count - 1)

