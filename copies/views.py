from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import CopieSerializer
from .mixins import CreateCopieMixin
from books.permissions import CustomBookPermission


# Create your views here.
class CopieView(CreateCopieMixin, CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomBookPermission]

    serializer_class = CopieSerializer
