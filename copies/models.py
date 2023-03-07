from django.db import models
import datetime

# Create your models here.


"""
    1. Adicionar nome da tabela de emprestimos
"""


class Copie(models.Model):
    class Meta:
        ordering = ("id",)

    book = models.ForeignKey(
        "books.Book", related_name="copies", on_delete=models.CASCADE
    )
    users = models.ManyToManyField(
        "users.User",
        through="copies.<nome_da_tabela_de_emprestimos>",
        related_name="loans",
    )
    is_available = models.BooleanField(default=True)
