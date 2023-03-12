from rest_framework import serializers
from .models import Book, Follow
from rest_framework import serializers
from users.serializers import UserSerializer
from copies.models import Copie


class BookSerializer(serializers.ModelSerializer):
    copies_qnt = serializers.IntegerField(min_value=1, write_only=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "description",
            "author",
            "copies_qnt",
            "is_available",
            "will_be_available_date",
        ]
        read_only_fields = ["will_be_available_date"]

    def create(self, validated_data: dict):
        copies_qnt = validated_data.pop("copies_qnt")
        book = Book.objects.create(**validated_data)
        copies_objects = [Copie(book=book) for _ in range(copies_qnt)]
        Copie.objects.bulk_create(copies_objects)

        return book

class FollowSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = [
            "id",
            "user",
            "created_at",
        ]
        read_only_fields = ["created_at"]
        depth = 1
