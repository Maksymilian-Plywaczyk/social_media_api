from rest_framework.serializers import ModelSerializer
from .models import User, Post, Comment


# Create serializers of User, Post, Comment
class UserLoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password')


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'user_type')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if validated_data['user_type'] == 'superuser':
            user = User.objects.create_superuser(
                email=validated_data['email'],
                password=validated_data['password'])
            return user
        else:
            user = User.objects.create_user(
                email=validated_data['email'],
                password=validated_data['password']
            )
            return user


class CommentSerializer(ModelSerializer):
    class Meta:
        ordering = ['-created_at']
        model = Comment
        fields = "__all__"


class PostSerializer(ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        ordering = ['-created_at']
        model = Post
        fields = ('id', 'title', 'content', 'author_id', 'comments')
