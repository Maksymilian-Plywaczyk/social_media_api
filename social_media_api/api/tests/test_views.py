from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from ..models import Post

User = get_user_model()


class RegisterAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('register')

    def test_register_user(self):
        data = {'email': 'test@example.com', 'password': 'test', 'user_type': 'normal'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
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


class PostViewSetTests(APITestCase):
    def setUp(self):
        self.url = reverse('post-list')
        self.user1 = User.objects.create_user(
            email='test1@test.com', password='testpassword1'
        )
        self.post = Post.objects.create(
            title='test title', content='test content', author_id=self.user1
        )

    def test_read_posts(self):
        response = self.client.get(self.url)
        posts = response.data["results"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(posts), 1)


class PostCreateAPIViewTestCase(APITestCase):
    def setUp(self):
        self.create_post_url = reverse('post_create')
        self.user = User.objects.create_superuser(
            email='admin@test.com',
            password='password',
        )

    def test_only_superusers_can_create_post_with_comments(self):
        # test when a non-superuser attempts to create a post
        self.client.force_authenticate(user=None)
        response = self.client.post(self.create_post_url, {'title': 'Test Post'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.count(), 0)

        # test when a superuser creates a post successfully
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.create_post_url,
            {
                "title": "title test",
                "content": "content test",
                "author_id": 1,
                "comments": [],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().comments.count(), 0)

    def test_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.create_post_url,
            {'title': 'Test Post', 'comments': [{'invalid_field': 'invalid_value'}]},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 0)


class PostUpdateAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='test')
        self.post = Post.objects.create(
            title='Test Post', content='Test Body', author_id=self.user
        )
        self.update_post_url = reverse('post_update', kwargs={'pk': self.post.pk})

    def test_post_update_by_owner(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            self.update_post_url,
            {
                "title": "title test",
                "content": "content test",
                "author_id": 1,
                "comments": [],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.get(id=self.post.id).title, 'title test')

    def test_post_update_by_non_owner(self):
        user = User.objects.create_user(email='nonowner@example.com', password='testpass')
        self.client.force_authenticate(user=user)
        response = self.client.put(self.update_post_url, {'title': 'Updated Title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
