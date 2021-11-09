from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.http import Http404

from functools import update_wrapper



def admin_view(view, cacheable=False):
    def inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404()
        return view(request, *args, **kwargs)

    if not cacheable:
        inner = never_cache(inner)

    # We add csrf_protect here so this function can be used as a utility
    # function for any view, without having to repeat 'csrf_protect'.
    if not getattr(view, 'csrf_exempt', False):
        inner = csrf_protect(inner)

    return update_wrapper(inner, view)
