from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import CommentForm, RecipeForm
from .models import Category, Comment, Favorite, Recipe


def home(request):
    """
    Главная страница:
    - блок сезонных блюд;
    - блок последних рецептов.
    """
    query = request.GET.get("q", "").strip()
    seasonal_recipes = Recipe.objects.filter(is_seasonal=True)[:4]
    latest_recipes = Recipe.objects.order_by("-created_at")
    if query:
        latest_recipes = latest_recipes.filter(title__icontains=query)
    latest_recipes = latest_recipes[:6]
    context = {
        "seasonal_recipes": seasonal_recipes,
        "latest_recipes": latest_recipes,
        "search_query": query,
    }
    return render(request, "recipes/home.html", context)


def category_recipes(request, slug):
    """
    Страница списка рецептов в выбранной категории.
    """
    category = get_object_or_404(Category, slug=slug)
    recipes = category.recipes.select_related("author", "category")
    context = {
        "category": category,
        "recipes": recipes,
    }
    return render(request, "recipes/category_list.html", context)


def recipe_detail(request, pk):
    """
    Страница отдельного рецепта:
    - отображение информации о рецепте;
    - список комментариев;
    - форма добавления комментария;
    - состояние избранного для текущего пользователя.
    """
    recipe = get_object_or_404(
        Recipe.objects.select_related("author", "category"),
        pk=pk,
    )
    comments = recipe.comments.select_related("author")

    # По умолчанию форма комментария пустая
    comment_form = CommentForm()

    # Обработка добавления комментария
    if request.method == "POST":
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.author = request.user
                comment.recipe = recipe
                comment.save()
                return redirect("recipes:detail", pk=recipe.pk)
        else:
            # Неавторизованных отправляем на страницу входа
            return redirect(f"{reverse('users:login')}?next={request.path}")

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(
            user=request.user, recipe=recipe
        ).exists()

    context = {
        "recipe": recipe,
        "comments": comments,
        "comment_form": comment_form,
        "is_favorite": is_favorite,
    }
    return render(request, "recipes/recipe_detail.html", context)


@login_required
def recipe_create(request):
    """
    Создание нового рецепта текущим пользователем.
    Заблокированным пользователям запрещено добавлять рецепты.
    """
    if getattr(request.user, "is_blocked", False):
        # Заблокированным пользователям запрещаем добавлять новые рецепты
        raise PermissionDenied("Ваш аккаунт заблокирован администратором.")

    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect("recipes:detail", pk=recipe.pk)
    else:
        form = RecipeForm()

    return render(request, "recipes/recipe_form.html", {"form": form})


@login_required
def toggle_favorite(request, pk):
    """
    Добавление/удаление рецепта из избранного текущего пользователя.
    Ожидается POST-запрос.
    """
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.method == "POST":
        favorite_qs = Favorite.objects.filter(user=request.user, recipe=recipe)
        if favorite_qs.exists():
            # Если уже в избранном — удаляем
            favorite_qs.delete()
        else:
            # Иначе добавляем
            Favorite.objects.create(user=request.user, recipe=recipe)

    return redirect("recipes:detail", pk=recipe.pk)


@login_required
def favorites_list(request):
    """
    Страница со списком избранных рецептов пользователя.
    """
    favorites = (
        Favorite.objects.filter(user=request.user)
        .select_related("recipe__author", "recipe__category")
        .order_by("-created_at")
    )
    context = {
        "favorites": favorites,
    }
    return render(request, "recipes/favorites.html", context)

