from .models import Book, Follow
from rest_framework.views import Response, Request
from django.shortcuts import get_object_or_404

class CustomFollowMixin:
    def post(self, request: Request, *args, **kwargs: dict):
        book = get_object_or_404(Book, id=kwargs.get("pk"))

        try:
            followers = Follow.objects.get(book=book, user=request.user)
            if followers:
                return Response({"message": "User already follow this book."}, 409)
        except Follow.DoesNotExist:
            pass

        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id, book_id=self.kwargs.get("pk"))
