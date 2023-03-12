from rest_framework import serializers
from .models import Copie, Loan
from datetime import timedelta, date
from books.serializers import BookSerializer


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
        loan_obj = Loan.objects.create(**validated_data)

        copie = validated_data["copie"]
        copie.is_available = False
        copie.save()
        if not copie.book.is_available:
            exp_date = (
                Loan.objects.filter(copie__book=copie.book, delivery_date=None)
                .first()
                .expected_return_date
            )
            loan_obj.copie.book.will_be_available_date = exp_date
            loan_obj.copie.book.save()
        return loan_obj

    def update(self, instance, validated_data):
        instance.delivery_date = validated_data["delivery_date"]
        instance.copie.is_available = True
        instance.copie.save()
        instance.copie.book.is_available = True
        instance.copie.book.will_be_available_date = None
        instance.copie.book.save()
        instance.save()
        # # Aqui--
        # print(instance.expected_return_date, "AQUIIIIII")
        # date_e = datetime(instance.expected_return_date)
        # if date_e < date.today():
        #     instance.user.is_blocked_date = date.today() + timedelta(days=7)
        #     instance.save()
        # até aqui
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
