from rest_framework import serializers
from .models import Copie, Loan
from users.models import User
from users.serializers import UserSerializer
from django.shortcuts import get_object_or_404
from datetime import timedelta, date, datetime
from books.models import Book
from rest_framework.views import Request, Response, status
from django import http


class CopieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Copie
        fields = [
            "id",
            "book",
            "is_available",
        ]
        read_only_fields = ["id", "book"]


class LoanSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    copie = CopieSerializer(read_only=True)

    def create(self, validated_data):
        email = validated_data.pop("email")

    def create(self, validated_data: dict):
        copie_id = validated_data.get("copie_id")
        copie = get_object_or_404(Loan, id=copie_id)
        user_id = validated_data["user_id"]
        user = get_object_or_404(User, id=user_id)
        current_day = datetime.now()
        return ""

    def get_expected_return_date(self, obj):
        date_now = date.today()
        after_3_days = date_now + timedelta(days=3)
        return_date = after_3_days

        if after_3_days.weekday() == 5:
            return_date += timedelta(days=2)
        if after_3_days.weekday() == 6:
            return_date += timedelta(days=1)
        validated_data["expected_return_date"] = return_date
        print(validated_data)
        return Loan.objects.create(**validated_data)
        # email = validated_data.pop("email")
        # book = validated_data.pop("book")
        # user = get_object_or_404(User, email=email)
        # user_has_open_book = Loan.objects.filter(user_id=user.id, delivery_date__isnull=True)
        # if user_has_open_book.exists():
        #     # return Response({"message": "Deliver borrowed book to make new loan"}, 204)
        #     raise serializers.ValidationError({"message": "Deliver borrowed book to make new loan"})

        # book_obj = get_object_or_404(Book, pk=book)
        # copie_is_available_true = Copie.objects.filter(
        #     book_id=book_obj.id, is_available=True
        # ).first()
        # if copie_is_available_true:
        #     return Loan.objects.create(
        #         copie=copie_is_available_true, user=user, **validated_data
        #     )
        # else:
        #     return Response({"message": "book currently unavailable"}, 200)

    # def update(self, instance: Loan, validated_data) -> str:
    #     email = validated_data.pop("email")
    #     book = validated_data.pop("book")
    #     user = get_object_or_404(User, email=email)
    #     user_has_open_book = instance.objects.filter(
    #         user_id=user.id, delivery_date__isnull=True
    #     )
    #     if user_has_open_book.exists():
    #         user_has_open_book.first()["delivery_date"] = date.today()
    #         Loan.save(user_has_open_book)
    #         return Response({"message": "Successfully returned book"}, 200)

    # return instance

    user = UserSerializer(read_only=True)

    class Meta:
        model = Loan
        fields = [
            "email",
            "user",
            "copie",
            "loan_date",
            "expected_return_date",
            "delivery_date",
        ]

        depth = 1
        # validators = [
        #     serializers.UniqueTogetherValidator(
        #         queryset=model.objects.all(),
        #         fields=("user", "copie"),
        #         message="Deliver borrowed book to make new loan",
        #     ),
        # ]
        read_only_fields = [
            "loan_date",
            "delivery_date",
            "expected_return_date",
        ]
        read_only_fields = ["loan_date", "delivery_date", "copie"]
