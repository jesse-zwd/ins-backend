from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class JWTSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        # Add custom claims
        data['nickname'] = self.user.nickname
        data['avatar'] = self.user.avatar
        data['id'] = self.user.id
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['website'] = self.user.website
        data['bio'] = self.user.bio

        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "nickname", "avatar", "bio", "first_name", "last_name", "website")


class UserSignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(label="email", help_text="email", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="user exists")])
    password = serializers.CharField(style={'input_type': 'password'}, help_text="password", label="password", write_only=True)
    nickname = serializers.CharField(label="nickname", help_text="nickname", required=True, allow_blank=False)

    def validate(self, attrs):
        attrs["email"] = attrs["username"]
        return attrs

    class Meta:
        model = User
        fields = ("password", "username", "nickname")



