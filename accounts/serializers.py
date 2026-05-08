from rest_framework import serializers

from .models import LibraryManager


class LibraryManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryManager
        fields = ["id", "username", "email"]
