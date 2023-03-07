from django.shortcuts import get_object_or_404
from books.models import Book
from rest_framework.views import Request, Response, status
from .models import Copie
from .serializers import CopieSerializer
from books.serializers import BookSerializer


class CreateCopieMixin:
    def create(self, request: Request, *args, **kwargs):
        book_obj = get_object_or_404(Book, pk=kwargs["book_id"])
        serializer = CopieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        copies_qnt = request.data.pop("copies_qnt")
        copies_objects = [Copie(book=book_obj) for _ in range(copies_qnt)]
        Copie.objects.bulk_create(copies_objects)
        book_serializer = BookSerializer(book_obj)
        data = {
            "book": book_serializer.data,
            "copies_total": Copie.objects.filter(book=book_obj).count(),
        }

        return Response(data, status=status.HTTP_201_CREATED)
