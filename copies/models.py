from django.db import models

# Create your models here.


# Falta a model de Books para gerar a migração com a relação.
class Copie(models.Model):
    class Meta:
        ordering = ("id",)

    book = models.ForeignKey(
        "books.Book", related_name="copies", on_delete=models.CASCADE
    )
    is_available = models.BooleanField(default=True)
    users = models.ManyToManyField(
        "users.User", through="copies.CopieLoan", related_name="loans"
    )


class CopieLoan(models.Model):
    class Meta:
        ordering = ("id",)

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    copie = models.ForeignKey("copies.Copie", on_delete=models.CASCADE)
