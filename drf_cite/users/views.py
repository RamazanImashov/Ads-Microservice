from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from .serializers import (
    LoginSerializer,
    ForgotPasswordSerializer, UsersSerializer,
    RegisterFromEmailSerializer,
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsUserAuth
from rest_framework import generics
from .services import (
    RegisterService,
    LogoutService,
    ChangePasswordService,
    ForgotPasswordService,
    ForgotPasswordCompleteService,
)
from drf_spectacular.utils import extend_schema
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action

# Create your views here.

User = get_user_model()


@extend_schema(tags=['Profile'])
class UsersView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    pagination_class = None
    search_fields = ['name', 'description']
    http_method_names = ['get', 'head', "put", "patch"]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)


@extend_schema(tags=['Register'])
class RegisterFromEmailView(APIView):
    service = RegisterService()
    permission_classes = (AllowAny,)

    @extend_schema(
        description="A description of the endpoint",
        request=RegisterFromEmailSerializer,
        responses={200: RegisterFromEmailSerializer}
    )
    def post(self, request):
        data = request.data
        status_code = self.service.register_email(data)
        return Response({"data": "Good, Registration successful for email",
                         "status": status_code}, status=status_code)


@extend_schema(tags=['Login'])
class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)


@extend_schema(tags=['Logout'])
class LogoutView(APIView):
    permission_classes = (IsUserAuth,)
    service = LogoutService()

    def post(self, request):
        response, status_code = self.service.logout(request)
        return Response(response, status=status_code)


@extend_schema(tags=['Change Password'])
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ChangePasswordService.change_password(request=request)
        return Response({"data": "Пароль успешно обновлен",
                         "status": HTTP_201_CREATED}, status=HTTP_201_CREATED)


@extend_schema(tags=['Forgot Password'])
class ForgotPasswordView(generics.CreateAPIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        ForgotPasswordService.send_code(self=self, request=request)
        return Response({"data": "Код восстановления отправлен на ваш email.",
                         "status": HTTP_201_CREATED}, status=HTTP_201_CREATED)


@extend_schema(tags=['Forgot Password'])
class ForgotPasswordCompleteView(APIView):
    def post(self, request):
        ForgotPasswordCompleteService.complete_password(request=request)
        return Response({"data": "Пароль успешно обновлен.",
                         "status": HTTP_200_OK}, status=HTTP_200_OK)
