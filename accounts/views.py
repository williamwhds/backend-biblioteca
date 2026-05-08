from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny

from .models import LibraryManager
from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = LibraryManager.objects.all()

    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LoginView(ObtainAuthToken):
    permission_classes = (AllowAny,)
    parser_classes = [JSONParser]
