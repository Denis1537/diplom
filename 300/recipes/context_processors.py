from .models import Category


def categories(request):
    """
    Возвращает список категорий для отображения в меню навигации.
    """
    return {"categories": Category.objects.all()}

