from django import template

from product.models import Category

register = template.Library()


@register.inclusion_tag('main/partial/category_navbar.html')
def category_navbar():
    return {
        "category": Category.objects.active(),
    }
