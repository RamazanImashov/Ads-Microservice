from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

# Register your models here.

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'phone_number', 'is_active', 'is_staff']
    search_fields = ['username', 'email']
    model = User


admin.site.register(User, CustomUserAdmin)
