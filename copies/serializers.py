from rest_framework import serializers
from .models import Copie


class CopieSerializer(serializers.ModelSerializer):
    copies_qnt = serializers.IntegerField(min_value=1, write_only=True)

    class Meta:
        model = Copie
        fields = [
            "id",
            "book",
            "is_available",
            "copies_qnt",
        ]
        read_only_fields = ["id", "book"]
