from .models import Book, Follow
from .serializers import BookSerializer, FollowSerializer
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    DestroyAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import CustomBookPermission
from .pagination import CustomBookPagination
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated
from .mixins import CustomFollowMixin
from django.shortcuts import get_object_or_404
from copies.exceptions import CustomDoesNotExists
from django.http import Http404


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


class FollowView(CustomFollowMixin, CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class DestroyFollowView(DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Follow.objects.all()
    book_queryset = Book.objects.all()
    serializer_class = FollowSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            "Expected view %s to be called with a URL keyword argument "
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            "attribute on the view correctly."
            % (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        try:
            book_obj = get_object_or_404(self.book_queryset, **filter_kwargs)
        except Http404:
            raise CustomDoesNotExists("Book not found.")

        try:
            follow_obj = get_object_or_404(
                queryset, user=self.request.user, book=book_obj
            )
        except Http404:
            raise CustomDoesNotExists("User does not follow this book.")
        # May raise a permission denied
        self.check_object_permissions(self.request, self.request.user)

        return follow_obj
