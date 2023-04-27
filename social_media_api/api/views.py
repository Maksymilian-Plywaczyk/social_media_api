from django.contrib.auth import login
from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.models import AuthToken
from .serializers import UserLoginSerializer, RegisterSerializer, PostSerializer, CommentSerializer
from knox.views import LoginView
from .models import Post


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": UserLoginSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        }, status=status.HTTP_201_CREATED)


class LoginAPI(LoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class PostCreateAPIView(generics.GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'message': 'Only superusers can create a post with comments'},
                            status=status.HTTP_403_FORBIDDEN)

        post_serializer = self.get_serializer(data=request.data)
        if post_serializer.is_valid(raise_exception=True):
            post = post_serializer.save()
            comments_data = request.data.get('comments', [])
            comments = []
            for comment_data in comments_data:
                comment_data['post_id'] = post.id
                comment_serializer = CommentSerializer(data=comment_data)
                if comment_serializer.is_valid():
                    comment_serializer.save()
                    comments.append(comment_serializer.data)
                else:

                    post.delete()
                    return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            post_serializer.data['comments'] = comments
            return Response(post_serializer.data, status=status.HTTP_201_CREATED)


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author_id == request.user


class PostUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Post.objects.filter(id=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        post_serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if post_serializer.is_valid():
            post = post_serializer.save()

            comments_data = request.data.get('comments', [])

            comments = []
            for comment_data in comments_data:
                comment_data['post_id'] = post.id
                comment_serializer = CommentSerializer(data=comment_data)
                if comment_serializer.is_valid():
                    comment_serializer.save()
                    comments.append(comment_serializer.data)
                else:
                    return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            post_serializer.data['comments'] = comments
            return Response(post_serializer.data, status=status.HTTP_200_OK)
