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
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    is_employee = serializers.BooleanField(allow_null=True, default=False)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "is_employee"]
        extra_kwargs = {"password": {"write_only": True}}
