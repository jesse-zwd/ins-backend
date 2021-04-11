from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.db.models import Q
from django.contrib.auth import get_user_model

from .models import Post, PostFile, Comment, Like, Follow, Save
from users.serializers import UserSerializer

User = get_user_model()


class FilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostFile
        fields = '__all__'

class PostPreviewSerializer(serializers.ModelSerializer):
    likesCount = serializers.SerializerMethodField()
    commentsCount = serializers.SerializerMethodField()
    files = serializers.SerializerMethodField()
 
    def get_commentsCount(self, instance):
        return Comment.objects.filter(Q(post=instance.id)).count()

    def get_likesCount(self, instance):
        return Like.objects.filter(Q(post=instance.id)).count()

    def get_files(self, instance):
        post_files = PostFile.objects.filter(Q(post=instance.id))
        files_serializer = FilesSerializer(post_files, many=True, read_only=True)
        return files_serializer.data

    class Meta:
        model = Post
        fields = ('id', 'likesCount', 'commentsCount', 'files')


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    files = serializers.SerializerMethodField()
    isLiked = serializers.SerializerMethodField()
    likesCount = serializers.SerializerMethodField()
    isSaved = serializers.SerializerMethodField()
    commentsCount = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    def get_files(self, instance):
        post_files = PostFile.objects.filter(Q(post=instance.id))
        files_serializer = FilesSerializer(post_files, many=True, read_only=True)
        return files_serializer.data

    def get_isLiked(self, instance):
        return Like.objects.filter(Q(post=instance.id) & Q(user=self.context["request"].user.id)).exists()

    def get_isSaved(self, instance):
        return Save.objects.filter(Q(post=instance.id) & Q(user=self.context["request"].user.id)).exists()

    def get_commentsCount(self, instance):
        return Comment.objects.filter(Q(post=instance.id)).count()

    def get_comments(self, instance):
        post_comments = Comment.objects.filter(Q(post=instance.id)).order_by('-createdAt')
        comments_serializer = CommentsSerializer(post_comments, many=True, read_only=True)
        return comments_serializer.data

    def get_likesCount(self, instance):
        return Like.objects.filter(Q(post=instance.id)).count()

    class Meta:
        model = Post
        fields = '__all__'


class FilesCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = PostFile
        fields = ('user', 'url')


class PostCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    files = FilesCreateSerializer(many=True, allow_null=True)

    def create(self, validated_data):
        files_data = validated_data.pop('files')
        post = Post.objects.create(**validated_data)
        if len(files_data) > 0:
            for file_data in files_data:
                PostFile.objects.create(post=post, **file_data)
        return post

    class Meta:
        model = Post
        fields = ('caption', 'user', 'files', 'tags')


class CommentsSerializer(serializers.ModelSerializer): 
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = '__all__'


class CommentCreateSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Comment
        fields = '__all__'


class LikesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'


class LikeCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Like
        validators = [
            UniqueTogetherValidator(
                queryset=Like.objects.all(),
                fields=('user', 'post'),
                message="已经点赞"
            )
        ]
        fields = ('user', 'post')


class FollowCreateSerializer(serializers.ModelSerializer):
    follower = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('following', 'follower'),
                message="已经关注"
            )
        ]
        fields = ('following', 'follower')


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = '__all__'


class SavesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Save
        fields = '__all__'


class SaveCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Save
        validators = [
            UniqueTogetherValidator(
                queryset=Save.objects.all(),
                fields=('user', 'post'),
                message="已经保存"
            )
        ]
        fields = ('user', 'post')


class UserProfileSerializer(serializers.ModelSerializer):
    isMe = serializers.SerializerMethodField()
    isFollowing = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()
    savedPosts = serializers.SerializerMethodField()
    postCount = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    followingCount = serializers.SerializerMethodField()
    followersCount = serializers.SerializerMethodField()

    def get_isMe(self, instance):
        return self.context['request'].user.id == instance.id

    def get_isFollowing(self, instance):
        return Follow.objects.filter(Q(following=instance.id) & Q(follower=self.context['request'].user.id)).exists()

    def get_postCount(self, instance):
        return Post.objects.filter(Q(user=instance.id)).count()
        
    def get_posts(self, instance):
        user_posts = Post.objects.filter(Q(user=instance.id)).order_by('-createdAt')
        userPosts_serializer = PostPreviewSerializer(user_posts, many=True, read_only=True)
        return userPosts_serializer.data  

    def get_followers(self, instance):
        user_Follows = Follow.objects.filter(Q(following=instance.id)).values()
        ids = []
        for f in user_Follows:
            ids.append(f['follower_id'])
        followers = User.objects.filter(Q(id__in=ids))
        userFollowers_serializer = UserSerializer(followers, many=True, read_only=True)
        return userFollowers_serializer.data

    def get_following(self, instance):
        user_Follows = Follow.objects.filter(Q(follower=instance.id)).values()
        ids = []
        for f in user_Follows:
            ids.append(f['following_id'])
        followings = User.objects.filter(Q(id__in=ids))
        userFollowings_serializer = UserSerializer(followings, many=True, read_only=True)
        return userFollowings_serializer.data

    def get_followingCount(self, instance):
        return Follow.objects.filter(Q(follower=instance.id)).count()

    def get_followersCount(self, instance):
        return Follow.objects.filter(Q(following=instance.id)).count()

    def get_savedPosts(self, instance):
        user_Saves = Save.objects.filter(Q(user=instance.id)).values()
        ids = []
        for s in user_Saves:
            ids.append(s['post_id'])
        saved_posts = Post.objects.filter(Q(id__in=ids)).order_by('-createdAt')
        savedPosts_serializer = PostPreviewSerializer(saved_posts, many=True, read_only=True)
        return savedPosts_serializer.data 

    class Meta:
        model = User
        fields = ("id", "avatar", "nickname", "bio", "website", "isMe", "postCount", "isFollowing", "following", "followers", "first_name", "last_name", "followersCount", "followingCount", "posts", "savedPosts")


