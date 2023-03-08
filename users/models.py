from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(max_length=127, unique=True)
    password = models.CharField(max_length=128)
    is_employee = models.BooleanField(null=True, default=False)
    is_blocked_date = models.DateTimeField(null=True, default=False)
