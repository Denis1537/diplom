from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """
    Админ-интерфейс пользователя:
    - отображение флага блокировки;
    - actions для массовой блокировки/разблокировки.
    """

    list_display = ("username", "email", "is_staff", "is_superuser", "is_blocked")
    list_filter = ("is_staff", "is_superuser", "is_active", "is_blocked")
    actions = ["block_users", "unblock_users"]

    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Блокировка", {"fields": ("is_blocked",)}),
    )

    @admin.action(description="Заблокировать выбранных пользователей")
    def block_users(self, request, queryset):
        """
        Отмечает поле is_blocked как True для выбранных пользователей.
        """
        queryset.update(is_blocked=True)

    @admin.action(description="Разблокировать выбранных пользователей")
    def unblock_users(self, request, queryset):
        """
        Сбрасывает флаг блокировки у выбранных пользователей.
        """
        queryset.update(is_blocked=False)

