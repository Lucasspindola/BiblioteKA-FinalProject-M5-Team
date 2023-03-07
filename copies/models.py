from django.db import models
import datetime
# Create your models here.

class CopieLoan(models.Model):
    class Meta:
        ordering = ("id",)

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    copie = models.ForeignKey("copies.Copie", on_delete=models.CASCADE)
    loan_date = models.DateTimeField(default=datetime.datetime.now())
    delivery_date = models.DateTimeField(null=True, blank=True)
    expected_return = models.DateTimeField()