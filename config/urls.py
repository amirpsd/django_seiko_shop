"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

# static
from django.conf.urls.static import static
from django.conf import settings


from permissions import admin_view
admin.site.admin_view = admin_view

# handler
from django.conf.urls import handler403, handler404
handler403 = 'config.utils.all_error_views.handler403'
handler404 = 'config.utils.all_error_views.handler404'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('product.urls')),
    path('', include('django.contrib.auth.urls')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('blog/', include('blog.urls')),
    path('contact/',include('contact.urls')),
    path('account/', include('account.urls')),
    path('account/favorite/', include('favorite_product.urls')),
    path('account/favorite/blog/', include('favorite_blog.urls')),
    path('comment/', include('comment.urls')),
    path('ckeditor', include('ckeditor_uploader.urls')),
]


if settings.DEBUG:
    # add root static files
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # add media static files
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
