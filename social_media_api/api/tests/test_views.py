from rest_framework.test import APITestCase, APIClient
from django.urls import reverse, resolve
from rest_framework import status
from django.contrib.auth import get_user_model
from ..models import Post, Comment
User = get_user_model()


class RegisterAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('register')

    def test_register_user(self):
        data = {'email': 'test@example.com', 'password': 'test', 'user_type': 'normal'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertIn('token', response.data)
        user_data = response.data['user']
        self.assertEqual(user_data['id'], 1)
        self.assertEqual(user_data['email'], 'test@example.com')


class LoginAPITestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.email = "test@example.com"
        self.password = "test"
        self.user = User.objects.create_user(email=self.email, password=self.password)
        self.url = reverse('login')

    def test_login_user(self):
        data = {'username': self.email, 'password': self.password}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'email': 'test@example.com', 'user_type': 'normal'})


class UserViewSetTests(APITestCase):
    def setUp(self):
        self.url = reverse('user-list')
        self.user1 = User.objects.create_user(email='test1@test.com', password='testpassword1')
        self.user2 = User.objects.create_user(email='test2@test.com', password='testpassword2')

    def test_read_users(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.url)
        users = response.data["results"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(users), 2)


class PostViewSetTests(APITestCase):
    def setUp(self):
        self.url = reverse('post-list')
        self.user1 = User.objects.create_user(email='test1@test.com', password='testpassword1')
        self.post = Post.objects.create(title='test title', content='test content', user=self.user1)

    def test_read_users(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.url)
        users = response.data["results"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(users), 1)
