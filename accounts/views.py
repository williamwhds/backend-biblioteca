from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import LibraryManager
from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = LibraryManager.objects.all()

    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
