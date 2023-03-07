from rest_framework import serializers
from .models import Book, Follow
from rest_framework import serializers
from users.serializers import UserSerializer

# from copies.models import Copies

"""
Necessário finalizar a model Copie para atualizar o método create.
"""


class BookSerializer(serializers.ModelSerializer):
    copies_qnt = serializers.IntegerField(min_value=0, write_only=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "description",
            "author",
            "copies_qnt",
            "is_avaliable",
        ]

    def create(self, validated_data: dict):
        copies_qnt = validated_data.pop("copies_qnt")
        book = Book.objects.create(**validated_data)
        # copies_objects = [Copies(book) for _ in range(copies_qnt)]

        # Copies.objects.bulk_create(copies_objects)

        return book


class FollowSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Follow
        fields = [
            "user",
            "book",
        ]
        depth = 1
