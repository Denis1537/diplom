from django.urls import path

from . import views

app_name = "recipes"

urlpatterns = [
    path("", views.home, name="home"),
    path("category/<slug:slug>/", views.category_recipes, name="category"),
    path("recipe/add/", views.recipe_create, name="add"),
    path("recipe/<int:pk>/", views.recipe_detail, name="detail"),
    path(
        "recipe/<int:pk>/favorite/",
        views.toggle_favorite,
        name="favorite_toggle",
    ),
    path("favorites/", views.favorites_list, name="favorites"),
]

