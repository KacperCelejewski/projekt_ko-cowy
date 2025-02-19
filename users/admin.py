# users/admin.py
from django.contrib import admin
from .models import User


# Rejestracja niestandardowego modelu użytkownika
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
    )
    search_fields = ("username", "email")
