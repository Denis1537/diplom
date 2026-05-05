from django import forms

from .models import Comment, Recipe


class RecipeForm(forms.ModelForm):
    """
    Форма создания/редактирования рецепта.
    Поле автора заполняется во вьюхе.
    """

    class Meta:
        model = Recipe
        fields = [
            "title",
            "description",
            "ingredients",
            "instructions",
            "image",
            "category",
            "is_seasonal",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "ingredients": forms.Textarea(
                attrs={"rows": 5, "placeholder": "Каждый ингредиент с новой строки"}
            ),
            "instructions": forms.Textarea(
                attrs={"rows": 6, "placeholder": "Опишите шаги приготовления"}
            ),
        }


class CommentForm(forms.ModelForm):
    """
    Форма для добавления комментария к рецепту.
    """

    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Напишите ваш комментарий...",
                }
            )
        }

