import random
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import ConfirmationCode
from .serializers import RegisterSerializer, ConfirmSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=False) 
        code = str(random.randint(100000, 999999))
        ConfirmationCode.objects.create(user=user, code=code)
        print(f"Код подтверждения: {code}")


class ConfirmUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ConfirmSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['code']
            try:
                confirm = ConfirmationCode.objects.get(code=code)
                user = confirm.user
                user.is_active = True
                user.save()
                confirm.delete()
                return Response({"message": "Пользователь подтверждён"}, status=status.HTTP_200_OK)
            except ConfirmationCode.DoesNotExist:
                return Response({"error": "Неверный код"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                    return Response({"error": "Неверный пароль"}, status=status.HTTP_400_BAD_REQUEST)

            if not user.is_active:
                    return Response({"error": "Пользователь не подтверждён"}, status=status.HTTP_403_FORBIDDEN)

            refresh = RefreshToken.for_user(user)
            return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                })
        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)
