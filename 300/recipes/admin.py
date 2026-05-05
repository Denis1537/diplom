from django.contrib import admin

from .models import Category, Comment, Favorite, Recipe


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """
    Админ-интерфейс рецептов:
    - удобный список с автором, категорией и признаком сезонности;
    - action для удаления выбранных рецептов.
    """

    list_display = ("title", "author", "category", "is_seasonal", "created_at")
    list_filter = ("category", "is_seasonal", "created_at")
    search_fields = ("title", "description", "ingredients")
    autocomplete_fields = ("author", "category")
    actions = ["delete_selected_recipes"]

    @admin.action(description="Удалить выбранные рецепты")
    def delete_selected_recipes(self, request, queryset):
        """
        Удаляет выбранные рецепты из базы данных.
        """
        queryset.delete()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("recipe", "author", "created_at")
    list_filter = ("created_at",)
    search_fields = ("text",)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe", "created_at")
    autocomplete_fields = ("user", "recipe")

