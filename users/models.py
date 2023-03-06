from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(max_length=127, unique=True)
    is_employee = models.BooleanField(null=True, default=False)
