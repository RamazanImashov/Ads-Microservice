from django.urls import path, include
from .views import (
    RegisterFromEmailView,
    RegisterFromPhoneView,
    LogoutView,
    ChangePasswordView,
    ForgotPasswordView,
    ForgotPasswordCompleteView,
    UsersProView,
    UsersView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()

routers.register("Profile", UsersProView, basename="profile")
routers.register("user", UsersView, basename="users")


urlpatterns = [
    path("", include(routers.urls)),
    path("register_email/", RegisterFromEmailView.as_view()),
    path("register_phone/", RegisterFromPhoneView.as_view()),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="auth_logout"),
    path("change_password/", ChangePasswordView.as_view()),
    path("lose_password/", ForgotPasswordView.as_view()),
    path("lose_confirm_code/", ForgotPasswordCompleteView.as_view(), name="forgot"),
]
