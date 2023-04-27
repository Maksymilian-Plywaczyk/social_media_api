from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext as _
from django.contrib.auth.hashers import make_password


class CustomUserManager(UserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        if not email:
            raise ValueError("User must have an email address")
        if not password:
            raise ValueError("User must have a password")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('user_type', 'superuser')
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("user_type") != 'superuser':
            raise ValueError("Superuser must have user_type=superuser")
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    SUPER_USER = "superuser"
    NORMAL_USER = "normal"
    USER_TYPES = [(SUPER_USER, _('Super user type')), (NORMAL_USER, _('Normal user type'))]

    username = None
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default=NORMAL_USER)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    @property
    def comments(self):
        return self.post_comments.all()


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    likes = models.ManyToManyField(User, related_name="liked_comments")
