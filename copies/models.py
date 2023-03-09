from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.


class Copie(models.Model):
    class Meta:
        ordering = ("id",)

    book = models.ForeignKey(
        "books.Book", related_name="copies", on_delete=models.CASCADE
    )
    loan_users = models.ManyToManyField(
        "users.User",
        through="copies.Loan",
        related_name="loans",
    )
    is_available = models.BooleanField(default=True)


class Loan(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    copie = models.ForeignKey("copies.Copie", on_delete=models.CASCADE)
    loan_date = models.DateTimeField(auto_now_add=True)
    expected_return_date = models.DateField()
    delivery_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ("id",)
        unique_together = ("user", "copie")

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
        except ValidationError as e:
            if "unique_together" in e.error_dict:
                raise ValidationError("This user already has a loan of this book")
            else:
                raise ValidationError("This user already has a loan of this book")
        super().save(*args, **kwargs)
