from rest_framework import serializers

from .models import CopieLoan
from users.models import User
from models import Copie
from django.shortcuts import get_object_or_404
from datetime import timedelta, date
import datetime


class CopieLoanSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict):
        copie_id = validated_data.get("copie_id")
        copie = get_object_or_404(Copie, id=copie_id)
        user_id = validated_data["user_id"]
        user = get_object_or_404(User, id=user_id)
        current_day = datetime.now()
        # Cada livro só poderá ser emprestado por um período fixo de tempo
        # Deverá ser criada uma lógica onde, se a devolução cair em um fim de semana (sábado ou domingo),
        # a data de retorno deverá ser modificada para ser no próximo dia útil
        max_loan_period = timedelta(days=7)
        expected_return = current_day + max_loan_period
        if expected_return.weekday() >= 5:  # sábado é 5 e domingo é 6
            expected_return = expected_return + timedelta(
                days=(7 - expected_return.weekday())
            )
        
        # Todos os livros emprestados deverão ter uma data de retorno

        # Caso o estudante não devolva o livro até o prazo estipulado,
        # deverá ser impedido (bloqueado) de solicitar outros empréstimos.

        # Se um estudante não efetuar a devolução dos livros no prazo estipulado,
        # ele não poderá emprestar mais livros até completar a devolução dos anteriores.
        # Após completar as devoluções pendentes, o bloqueio deve permanecer por alguns dias.
        return ""

    class Meta:
        model = CopieLoan
        fields = [
            "id",
            "loan_date",
            "delivery_date",
            "expected_return",
            "user_id",
            "copie_id",
        ]
