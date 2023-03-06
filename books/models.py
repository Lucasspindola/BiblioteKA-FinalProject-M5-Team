from django.db import models


class Book(models.Model):

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

    follower = models.ManyToManyField(
        "users.User", through="Follow", related_name="books")


class Follow(models.Model):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="user_book_follow")
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="book_follow")
    borrowed_at = models.DateTimeField(auto_now_add=True)
    # price = models.DecimalField(max_digits=8, decimal_places=2)
