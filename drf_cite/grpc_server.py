import os
import grpc
import django
from concurrent import futures
import user_pb2
import user_pb2_grpc

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.setting.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.exceptions import AuthenticationFailed

CustomUser = get_user_model()


# Функция аутентификации токена
def authenticate_token(token: str):
    jwt_authenticator = JWTAuthentication()
    try:
        validated_token = jwt_authenticator.get_validated_token(token)
        user = jwt_authenticator.get_user(validated_token)
        print("Authenticated user:", user.username, "-", user.id)
        return user  # Вернет объект пользователя, если токен действителен
    except AuthenticationFailed as e:
        print("Token authentication failed:", str(e))
        return None


# Класс сервиса gRPC
class UserService(user_pb2_grpc.UserServiceServicer):

    def GetUser(self, request, context):
        try:
            user = CustomUser.objects.get(id=request.user_id)
            print("GetUser found user:", user.username, "-", user.id)
            return user_pb2.UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                is_valid=True
            )
        except CustomUser.DoesNotExist:
            print("GetUser: User not found")
            return user_pb2.UserResponse(is_valid=False)

    def CheckVerifyToken(self, request, context):
        token = request.token
        user = authenticate_token(token)
        if user:
            return user_pb2.TokenResponse(id=user.id, username=user.username, email=user.email, is_valid=True)
        return user_pb2.TokenResponse(is_valid=False)


# Запуск gRPC сервера
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
