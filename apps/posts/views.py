from rest_framework import mixins, viewsets, permissions, filters
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model

from .serializers import UserProfileSerializer, PostCreateSerializer, PostSerializer, CommentCreateSerializer, CommentsSerializer, FollowCreateSerializer, FollowSerializer, LikeCreateSerializer, LikesSerializer, SaveCreateSerializer, SavesSerializer, PostPreviewSerializer
from .models import Post, Comment, Follow, Like, Save
from users.serializers import UserSerializer

User = get_user_model()

# Create your views here.

class PostViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    queryset = Post.objects.all().order_by('-createdAt')
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer

        return PostSerializer


class PostSearchViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    queryset = Post.objects.all().order_by('-createdAt')
    serializer_class = PostPreviewSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('caption', 'tags')


class CommentViewset(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Comment.objects.all().order_by('-createdAt')

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        
        return CommentsSerializer


class FollowViewset(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'following_id'
    
    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return FollowCreateSerializer
        
        return FollowSerializer


class LikeViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    authentication_classes = (JWTAuthentication, SessionAuthentication )
    permission_classes = (permissions.IsAuthenticated,) 
    lookup_field = 'post_id'

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return LikeCreateSerializer
        
        return LikesSerializer


class SaveViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    authentication_classes = (JWTAuthentication, SessionAuthentication )
    permission_classes = (permissions.IsAuthenticated,) 
    lookup_field = 'post_id'

    def get_queryset(self):
        return Save.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return SaveCreateSerializer
        
        return SavesSerializer
 

class FeedViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = (JWTAuthentication, SessionAuthentication )
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PostSerializer

    def get_queryset(self):
        follows = Follow.objects.filter(follower=self.request.user).values()
        ids = []
        for f in follows:
            ids.append(f['following_id'])
        ids.append(self.request.user.id)

        return Post.objects.filter(user__in=ids).order_by('-createdAt')


class UserProfileViewset(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,) 
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'update':
            return UserSerializer

        return UserProfileSerializer