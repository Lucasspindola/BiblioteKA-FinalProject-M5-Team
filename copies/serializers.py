from rest_framework import serializers
from .models import Copie, Loan
from users.models import User
from django.shortcuts import get_object_or_404
from datetime import timedelta, date, datetime


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


class LoanSerializer(serializers.ModelSerializer):
    expected_return_date = serializers.SerializerMethodField()

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

        return return_date

    class Meta:
        model = Loan
        fields = [
            "user",
            "copie",
            "loan_date",
            "expected_return_date",
            "delivery_date",
        ]
        read_only_fields = ["loan_date", "delivery_date", "copie"]
