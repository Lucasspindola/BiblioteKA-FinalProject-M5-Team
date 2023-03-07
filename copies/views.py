from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import CopieSerializer
from .mixins import CreateCopieMixin


# Create your views here.
class CopieView(CreateCopieMixin, CreateAPIView):
    serializer_class = CopieSerializer
