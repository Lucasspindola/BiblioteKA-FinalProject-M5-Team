from django.shortcuts import render
from .models import Book
from .serializers import BookSerializer
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView


class BookView(CreateAPIView):

    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetailView(RetrieveUpdateDestroyAPIView):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
