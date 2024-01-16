from django import template
from mint_app.models import Category


register = template.Library()


@register.simple_tag()
def tag_categories():
    return Category.objects.all()
