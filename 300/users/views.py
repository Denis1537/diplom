from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from recipes.models import Recipe

from .forms import LoginForm, RegistrationForm


def register(request):
    """
    Регистрация нового пользователя.
    После успешной регистрации сразу выполняется вход.
    """
    if request.user.is_authenticated:
        return redirect("users:profile")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("users:profile")
    else:
        form = RegistrationForm()

    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):
    """
    Личный кабинет пользователя с перечнем его рецептов.
    """
    user_recipes = Recipe.objects.filter(author=request.user)
    context = {
        "user_recipes": user_recipes,
    }
    return render(request, "users/profile.html", context)

