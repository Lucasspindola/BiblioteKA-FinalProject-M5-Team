from django.shortcuts import render
from .models import Book, Follow
from .serializers import BookSerializer, FollowSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import CustomBookPermission
from .pagination import CustomBookPagination
from django_filters import rest_framework as filters
from rest_framework.views import Response
from rest_framework.permissions import IsAuthenticated


class BookFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    author = filters.CharFilter(field_name="author", lookup_expr="icontains")


class BookView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomBookPermission]

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    pagination_class = CustomBookPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter


class BookDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomBookPermission]

    queryset = Book.objects.all()
    serializer_class = BookSerializer


class FollowView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def post(self, request, *args, **kwargs):

        book = Book.objects.get(id=self.kwargs.get("pk"))
        try:
            followers = Follow.objects.get(book=book, user=request.user)
            if followers:
                return Response({"message": "Usuario já segue esse livro"}, 409)
        except Follow.DoesNotExist:
            pass

        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):

        serializer.save(user_id=self.request.user.id,
                        book_id=self.kwargs.get("pk"))
