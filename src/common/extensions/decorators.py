from django.utils.html import format_html

from functools import wraps


def format_image(func):
    @wraps(func)
    def wrapper(instance):
        title, image = func(instance)
        result = format_html(f"<img src='{image}' alt='{title}' width='100px' height='60px' style='border-radius: 5px'>")
        return result

    return wrapper
