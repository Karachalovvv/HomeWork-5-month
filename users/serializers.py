import random
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import ConfirmationCode


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_username(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Имя пользователя не может быть пустым.")
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("Пользователь с таким username уже существует.")
        return value

    def validate_email(self, value):
        value = value.strip()
        if value and User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        return value

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            is_active=False
        )
        user.set_password(validated_data['password'])
        user.save()

        # генерируем 6-значный код
        code = f"{random.randint(100000, 999999)}"
        ConfirmationCode.objects.create(user=user, code=code)

        # тут можно отправить email/SMS, а пока:
        print(f"[DEBUG] Код подтверждения для {user.username}: {code}")

        return user


class ConfirmSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        username = attrs.get('username')
        code = attrs.get('code')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден.")

        try:
            cc = user.confirmation_code
        except ConfirmationCode.DoesNotExist:
            raise serializers.ValidationError("Код подтверждения не найден. Запросите повторную регистрацию.")

        if cc.code != code:
            raise serializers.ValidationError("Неверный код подтверждения.")

        attrs['user'] = user
        attrs['cc'] = cc
        return attrs

    def save(self, **kwargs):
        user = self.validated_data['user']
        cc = self.validated_data['cc']
        user.is_active = True
        user.save()
        cc.delete()
        return user