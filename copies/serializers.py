from rest_framework import serializers
from .models import Copie


class CopieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Copie
        fields = [
            "id",
            "book_id",
            "is_available",
        ]
