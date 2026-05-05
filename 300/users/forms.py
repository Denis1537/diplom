from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class RegistrationForm(UserCreationForm):
    """
    Форма регистрации нового пользователя.
    """

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class LoginForm(AuthenticationForm):
    """
    Форма входа с проверкой на блокировку пользователя.
    """

    def confirm_login_allowed(self, user):
        """
        Запрещаем вход заблокированным пользователям.
        """
        super().confirm_login_allowed(user)
        if getattr(user, "is_blocked", False):
            raise forms.ValidationError(
                "Ваш аккаунт заблокирован администратором.",
                code="blocked",
            )

