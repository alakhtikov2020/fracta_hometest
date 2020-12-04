from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class MessageBusViewSetTest(APITestCase):

    def setUp(self):
        self.token_obtain_pair_url = reverse('token_obtain_pair')
        self.user_info_url = reverse('user_info-list')

        User.objects.create_user(username='user1', password='password1', email='user1@test.com')
        User.objects.create_user(username='user2', password='password2', email='user2@test.com')

        data = {
            'username': 'user1',
            'password': 'password1'
        }
        response = self.client.post(self.token_obtain_pair_url, data, format='json')
        access_token = response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def test_get_user_info_happy_path(self):
        """
        current_user_id == id
        /api/user/?id=1
        """
        response = self.client.get(self.user_info_url + '?id=1', format='json')
        response_json = response.json()[0]
        username = response_json['username']
        email = response_json['email']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(username, 'user1')
        self.assertEqual(email, 'user1@test.com')

    def test_get_user_info_wrong_id_format(self):
        """
        /api/user/
        /api/user/?id=abc
        /api/user/?id=3.14
        """
        response = self.client.get(self.user_info_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.get(self.user_info_url + '?id=abc', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.get(self.user_info_url + '?id=3.14', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_info_access_other_id(self):
        """
        current_user_id == 1
        /api/user/?id=2
        """
        response = self.client.get(self.user_info_url + '?id=2', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_info_unauthorized(self):
        """
        AUTHORIZATION: ''
        /api/user/?id=1
        """
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.get(self.user_info_url + '?id=1', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
