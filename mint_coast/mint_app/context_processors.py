from .models import Category


def categories_proc(request):
    return {'categories': Category.objects.all()}
