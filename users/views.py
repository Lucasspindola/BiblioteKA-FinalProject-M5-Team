from .models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import CreateAPIView


class UserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer