from .models import Category

def list_categoryes(request):
    """Список категорий в меню
    отображается на всех страницах"""
    return {"menu_categoryes": Category.objects.all()}