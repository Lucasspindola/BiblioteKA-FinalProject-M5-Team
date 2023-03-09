from django.shortcuts import get_object_or_404
from books.models import Book
from rest_framework.views import Request, Response, status
from .models import Copie
from books.serializers import BookSerializer
from django.core.exceptions import ValidationError
from django.http import Http404
from datetime import date


class CreateCopieMixin:
    def create(self, request: Request, *args, **kwargs):
        book_obj = get_object_or_404(Book, pk=kwargs["book_id"])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        copies_qnt = request.data.pop("copies_qnt")
        copies_objects = [Copie(book=book_obj) for _ in range(copies_qnt)]
        Copie.objects.bulk_create(copies_objects)
        book_serializer = BookSerializer(book_obj)
        data = {
            "book": book_serializer.data,
            "copies_created": copies_qnt,
            "copies_total": Copie.objects.filter(book=book_obj).count(),
        }

        return Response(data, status=status.HTTP_201_CREATED)


class CreateLoanMixin:
    book_queryset = None
    user_queryset = None

    def create(self, request, *args, **kwargs):
        assert self.book_queryset is not None, (
            "'%s' should either include a `book_queryset` attribute, "
            % self.__class__.__name__
        )

        assert self.user_queryset is not None, (
            "'%s' should either include a `user_queryset` attribute, "
            % self.__class__.__name__
        )

        serializer = self.get_serializer(
            data=self.request.data,
        )
        serializer.is_valid(raise_exception=True)
        email = self.request.data.pop("email")
        try:
            book_obj = get_object_or_404(self.book_queryset, pk=kwargs["pk"])
        except Http404:
            return Response(
                {"detail": f"{self.book_queryset.model.__name__} not found"}, 404
            )

        try:
            user_obj = get_object_or_404(self.user_queryset, email=email)
        except Http404:
            return Response(
                {"detail": f"{self.user_queryset.model.__name__} not found"}, 404
            )
        copies = Copie.objects.filter(book_id=book_obj.id, is_available=True)
        copie = copies.first()
        if copie:
            try:
                serializer.save(user=user_obj, copie=copie)
                copie.is_available = False
                copie.save()
            except ValidationError as err:
                return Response({"detail": err}, status=status.HTTP_409_CONFLICT)
        else:
            return Response(
                {"message": "Book currently unavailable"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateLoanMixin:
    book_queryset = None
    user_queryset = None

    def patch(self, request, *args, **kwargs):
        serializer_body_check = self.get_serializer(data=request.data)
        serializer_body_check.is_valid(raise_exception=True)
        return super().patch(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()  # retorna o Loan
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def get_object(self):
        assert self.book_queryset is not None, (
            "'%s' should either include a `book_queryset` attribute, "
            % self.__class__.__name__
        )

        assert self.user_queryset is not None, (
            "'%s' should either include a `user_queryset` attribute, "
            % self.__class__.__name__
        )

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            "Expected view %s to be called with a URL keyword argument "
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            "attribute on the view correctly."
            % (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {
            self.lookup_field: self.kwargs[lookup_url_kwarg]
        }  # Pegar o id do book

        book_obj = get_object_or_404(self.book_queryset, **filter_kwargs)
        user_obj = get_object_or_404(
            self.user_queryset, email=self.request.data["email"]
        )
        obj = get_object_or_404(self.queryset, user=user_obj, copie__book=book_obj)

        if not obj.delivery_date:
            obj.delivery_date = date.today()
        self.check_object_permissions(self.request, obj)

        return obj
