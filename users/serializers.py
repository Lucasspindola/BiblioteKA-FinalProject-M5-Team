from books.models import Book
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomJWTSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["is_employee"] = user.is_employee

        return token


class FollowBooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ["follower_users"]


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict) -> User:
        if not validated_data["is_employee"]:
            return User.objects.create_user(**validated_data)

        return User.objects.create_superuser(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        pass_word = validated_data.pop("password", None)

        instance.set_password(pass_word)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="A user with that email already exists.",
            )
        ],
    )
    is_employee = serializers.BooleanField(allow_null=True, default=False)

    following_books = FollowBooksSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "is_employee",
            "is_blocked_date",
            "following_books",
        ]
        read_only_fields = ["is_blocked_date"]
        extra_kwargs = {"password": {"write_only": True}}
        depth = 1
