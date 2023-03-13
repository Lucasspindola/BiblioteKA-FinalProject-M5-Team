from django.shortcuts import get_object_or_404
from books.models import Book
from rest_framework.views import Request, Response, status
from .models import Copie, Loan
from books.serializers import BookSerializer
from django.http import Http404
from datetime import date
from .exceptions import CustomDoesNotExists


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
        email = self.request.data.pop("email", None)
        try:
            book_obj = get_object_or_404(self.book_queryset, pk=kwargs["pk"])
        except Http404:
            return Response(
                {"detail": f"{self.book_queryset.model.__name__} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            user_obj = get_object_or_404(self.user_queryset, email=email)

            if (
                user_obj.is_blocked_date is not None
                and user_obj.is_blocked_date > date.today()
            ):
                return Response(
                    {"detail": f"User is blocked until {user_obj.is_blocked_date}."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            if (
                user_obj.is_blocked_date is not None
                and user_obj.is_blocked_date < date.today()
            ):
                user_obj.is_blocked_date = None
                user_obj.save()
        except Http404:
            return Response(
                {"detail": f"{self.user_queryset.model.__name__} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        copies = Copie.objects.filter(book_id=book_obj.id, is_available=True)
        copie = copies.first()
        if copies.count() < 2:
            book_obj.is_available = False
            book_obj.save()
        if copie:
            loan_exists = Loan.objects.filter(
                user=user_obj, copie__book=book_obj, delivery_date=None
            ).exists()
            if loan_exists:
                return Response(
                    {"detail": "This user already has a loan of this book."},
                    status=status.HTTP_409_CONFLICT,
                )
            serializer.save(user=user_obj, copie=copie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"detail": "Book currently unavailable."},
                status=status.HTTP_404_NOT_FOUND,
            )


class UpdateLoanMixin:
    book_queryset = None
    user_queryset = None

    def patch(self, request, *args, **kwargs):
        self.check_object_permissions(request, request.user)
        serializer_body_check = self.get_serializer(data=request.data)
        serializer_body_check.is_valid(raise_exception=True)
        return super().patch(request, *args, **kwargs)

    def get_object(self):
        assert self.book_queryset is not None, (
            "'%s' should either include a `book_queryset` attribute, "
            % self.__class__.__name__
        )

        assert self.user_queryset is not None, (
            "'%s' should either include a `user_queryset` attribute, "
            % self.__class__.__name__
        )

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
            raise CustomDoesNotExists(f"{self.book_queryset.model.__name__} not found.")

        try:
            user_obj = get_object_or_404(
                self.user_queryset, email=self.request.data["email"]
            )
        except Http404:
            raise CustomDoesNotExists(f"{self.user_queryset.model.__name__} not found.")

        loan_obj = get_object_or_404(
            self.queryset, user=user_obj, copie__book=book_obj, delivery_date=None
        )

        self.check_object_permissions(self.request, loan_obj)

        return loan_obj
