from rest_framework.serializers import ValidationError
from django.contrib.auth import get_user_model, authenticate
from .tasks import send_password_celery
from rest_framework import serializers


User = get_user_model()


class RegisterValidator:
    @staticmethod
    def validate(attrs):
        password = attrs.get("password")
        password_confirm = attrs.pop("password_confirm")
        if password != password_confirm:
            raise ValidationError("Password not confirm")
        return attrs

    @staticmethod
    def create(validated_data):
        return User.objects.create_user(**validated_data)



class LoginValidator:
    @staticmethod
    def validate(username):
        if not User.objects.filter(username=username).exists():
            raise ValidationError("User not found")
        return username

    @staticmethod
    def validate_user(self, attrs):
        request = self.context.get("request")
        username = attrs.get("email")
        password = attrs.get("password")

        if username and password:
            user = authenticate(username=username, password=password, request=request)

            if not user:
                raise ValidationError("Error username or password")

        else:
            raise ValidationError("Username and password obazatelno")

        attrs["user"] = user
        return attrs

    @staticmethod
    def validate_found_phone(phone_number):
        if not User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("User not found")
        return phone_number

    @staticmethod
    def validate_phone(self, attrs):
        request = self.context.get("request")
        phone_number = attrs.get("phone_number")
        password = attrs.get("password")

        if phone_number and password:
            user = authenticate(phone_number=phone_number, password=password, request=request)

            if not user:
                raise ValidationError("Error email or password")

        else:
            raise ValidationError("Username and password obazatelno")

        attrs["user"] = user
        return attrs


class ChangePasswordValidator:
    @staticmethod
    def validate_old_password(self, old_password):
        request = self.context.get("request")
        user = request.user
        if not user.check_password(old_password):
            raise serializers.ValidationError("Введите корректный пароль")
        return old_password

    @staticmethod
    def validate(attrs):
        old_password = attrs.get("old_password")
        new_password = attrs.get("new_password")
        new_password_confirm = attrs.get("new_password_confirm")

        if new_password != new_password_confirm:
            raise serializers.ValidationError("Пароли не совпадают")
        if new_password == old_password:
            raise serializers.ValidationError("Старый и новый пароли совпадают")
        return attrs

    @staticmethod
    def set_new_password(self):
        new_password = self.validated_data.get("new_password")
        user = self.context.get("request").user
        user.set_password(new_password)
        user.save()


class ForgotPasswordValidator:
    @staticmethod
    def validate(attrs):
        email = attrs.get("email")

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Пользователь с таким email не найден")
        return attrs

    @staticmethod
    def send_verification_email(self):
        email = self.validated_data.get("email")
        user = User.objects.get(email=email)
        user.create_activation_code()
        send_password_celery(user.username, user.email, user.activation_code)


class ForgotPasswordCompleteValidator:
    @staticmethod
    def validate(attrs):
        email = attrs.get("email")
        code = attrs.get("code")
        password = attrs.get("password")
        password_confirm = attrs.pop("password_confirm")

        if not User.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValidationError(
                "Пользователь не найден или неправильный код"
            )
        if password != password_confirm:
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs

    @staticmethod
    def set_new_password(self):
        email = self.validated_data.get("email")
        password = self.validated_data.get("password")
        user = User.objects.get(email=email)
        user.set_password(password)
        user.activation_code = ""
        user.save()
