from rest_framework import serializers
from .models import Copie, Loan
from datetime import timedelta, date
from books.serializers import BookSerializer
from datetime import timedelta, datetime


class CopieSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
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
        depth = 1


class LoanSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    copie = CopieSerializer(read_only=True)

    def create(self, validated_data):
        email = validated_data.pop("email")
        date_now = date.today()
        after_3_days = date_now + timedelta(days=3)
        return_date = after_3_days
        check_until_day = 7 - after_3_days.weekday()
        if after_3_days.weekday() > 4:
            return_date += timedelta(days=check_until_day)

        validated_data["expected_return_date"] = return_date
        return Loan.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.delivery_date = validated_data["delivery_date"]
        instance.copie.is_available = True
        instance.copie.save()
        instance.copie.book.is_available = True
        instance.copie.book.save()
        instance.save()

        date_e_str = instance.expected_return_date.strftime("%Y-%m-%d")
        date_e = datetime.strptime(date_e_str, "%Y-%m-%d")
        date_e_date = date_e.date()

        if date_e_date < date.today():
            instance.user.is_blocked_date = datetime.now() + timedelta(days=7)
            instance.user.save()

        return instance

    class Meta:
        model = Loan
        fields = [
            "id",
            "email",
            "loan_date",
            "expected_return_date",
            "delivery_date",
            "copie",
        ]
        read_only_fields = [
            "loan_date",
            "delivery_date",
            "expected_return_date",
            "copie",
        ]
        depth = 2
