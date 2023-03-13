from django.db import models


class Book(models.Model):
    class Meta:
        ordering = ("title",)

    title = models.CharField(
        max_length=255,
        unique=True,
        error_messages={
            "unique": ("A book with that title already exists."),
        },
    )
    description = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True)
    will_be_available_date = models.DateField(null=True, blank=True)
    follower_users = models.ManyToManyField(
        "users.User", through="Follow", related_name="following_books"
    )


class Follow(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
