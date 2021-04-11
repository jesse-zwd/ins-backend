from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import mixins, viewsets 

from .serializers import JWTSerializer, UserSignupSerializer
# Create your views here.

class LoginViewset(TokenObtainPairView):
    serializer_class = JWTSerializer


class SignupViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSignupSerializer


