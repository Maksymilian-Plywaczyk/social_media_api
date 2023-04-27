from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Comment, Post

# Create your tests here.


class UserTestCase(TestCase):
    def test_create_user_with_email_successful(self):
        email = "example@example.com"
        password = "test123"
        user = get_user_model().objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_superuser_with_email_successful(self):
        email = "example@example.com"
        password = "test123"
        super_user = get_user_model().objects.create_superuser(
            email=email, password=password
        )
        self.assertTrue(super_user.is_superuser, True)
        self.assertEqual(super_user.user_type, 'superuser')

    def test_str_user(self):
        email = "example@example.com"
        password = "test123"
        user = get_user_model().objects.create_user(email=email, password=password)
        self.assertEqual(str(user), email)

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=None, password="test123")

    def test_create_user_without_password(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email="example@example", password=None)


class PostTestCase(TestCase):
    def test_create_post_successful(self):
        user = get_user_model().objects.create_user(
            email="example@example.com", password="test123"
        )
        title = "Test title"
        content = "Test content"

        post = Post.objects.create(title=title, content=content, author_id=user)
        self.assertEqual(post.title, title)
        self.assertEqual(post.content, content)
        self.assertEqual(post.author_id, user)


class CommentTestCase(TestCase):
    def test_create_comment_successful(self):
        user = get_user_model().objects.create_user(
            email="example@example.com", password="test123"
        )
        post = Post.objects.create(
            title="Test title", content="Test content", user=user
        )

        content = "Test comment"

        comment = Comment.objects.create(content=content, author_id=user, post=post)
        self.assertEqual(comment.content, content)
        self.assertEqual(comment.author_id, user)
        self.assertEqual(comment.post, post)
