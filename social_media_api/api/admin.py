from django.contrib import admin
from .models import Post, Comment
from django.contrib.auth import get_user_model

# Register your models here.

User = get_user_model()

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
