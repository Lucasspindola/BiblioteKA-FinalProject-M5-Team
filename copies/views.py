from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.views import Request, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import CopieSerializer, LoanSerializer
from .mixins import CreateCopieMixin
from books.permissions import CustomBookPermission
from .models import Loan
from django.shortcuts import get_object_or_404
from users.models import User
from books.models import Book
from copies.models import Copie
from users.serializers import UserSerializer

# Create your views here.


class CopieView(CreateCopieMixin, CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomBookPermission]

    serializer_class = CopieSerializer


class LoansView(CreateAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = LoanSerializer
    queryset = Loan.objects.all()

    def create(self, request, *args, **kwargs):
        email = self.request.data.pop("email")
        book = self.kwargs["pk"]
        user = get_object_or_404(User, email=email)
        user_serializer = UserSerializer(user)
        book_obj = get_object_or_404(Book, pk=book)
        copie_is_available_true = Copie.objects.filter(
            book_id=book_obj.id, is_available=True
        ).first()
        print(copie_is_available_true, "AQUII")
        data = {"copie": copie_is_available_true, "user": user}
        if copie_is_available_true:
            serializer = LoanSerializer(
                data={
                    "email": email,
                    "user": user,
                    "copie": copie_is_available_true,
                }
            )
        else:
            return Response({"message": "book currently unavailable"}, 404)
        print(user, copie_is_available_true)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class LoansDetailsView(CreateAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = LoanSerializer
    queryset = Loan.objects.all()

    def perform_create(self, serializer):
        return serializer.save(book=self.kwargs["pk"])

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
