from .models import Book, Follow
from rest_framework.views import Response, Request, status


class CustomFollowMixin:
    def post(self, request: Request, *args, **kwargs: dict):
        try:
            book = Book.objects.get(id=kwargs.get("book_id"))
        except Book.DoesNotExist:
            return Response({"detail": "Book not found."}, status.HTTP_404_NOT_FOUND)

        try:
            followers = Follow.objects.get(book=book, user=request.user)
            if followers:
                return Response(
                    {"detail": "User already follow this book."},
                    status.HTTP_409_CONFLICT,
                )
        except Follow.DoesNotExist:
            pass

        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, book_id=self.kwargs.get("book_id"))
