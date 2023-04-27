"""
URL configuration for social_media_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from social_media_api.api import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("api/register/", views.RegisterAPI.as_view(), name="register"),
    path("api/login/", views.LoginAPI.as_view(), name="login"),
    path("api/", include(router.urls), name="api"),
    path("api/posts/create", views.PostCreateAPIView.as_view(), name="post_create"),
    path("api/posts/<int:pk>/update", views.PostUpdateAPIView.as_view(), name="post_update"),
]
