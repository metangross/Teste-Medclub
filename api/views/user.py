from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.serializers.user import UserSerializer


class UserView(GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        user = request.user
        user = UserSerializer(instance=user)
        return Response(data=user.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserListView(CreateAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = UserSerializer
    queryset = User.objects.all()


class LoginView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            token = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "Login realizado com sucesso.",
                    "access": str(token.access_token),
                }
            )

        return Response(
            {"message": "Falha ao fazer login."}, status=status.HTTP_401_UNAUTHORIZED
        )
