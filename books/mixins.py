from .models import Book, Follow
from rest_framework.views import Response, Request


class CustomFollowMixin:
    def post(self, request: Request, *args, **kwargs: dict):
        try:
            book = Book.objects.get(id=kwargs.get("pk"))
        except Book.DoesNotExist:
            return Response({"detail": "Book not found."}, 404)

        try:
            followers = Follow.objects.get(book=book, user=request.user)
            if followers:
                return Response({"message": "User already follow this book."}, 409)
        except Follow.DoesNotExist:
            pass

        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id, book_id=self.kwargs.get("pk"))
