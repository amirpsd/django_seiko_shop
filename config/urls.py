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
from config import settings
from django.conf.urls.static import static
from permissions import admin_view

admin.site.admin_view = admin_view

handler404 = 'seiko_shop.views.handler404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('seiko_shop.urls')),
    path('', include('django.contrib.auth.urls')),
    path('cart/', include('seiko_cart.urls', namespace='cart')),
    path('orders/', include('seiko_orders.urls', namespace='orders')),
    path('blog/', include('seiko_blog.urls')),
    path('contact/',include('seiko_contact.urls')),
    path('account/', include('seiko_account.urls')),
    path('account/favorite/', include('seiko_favorite_product.urls')),
    path('account/favorite/blog/', include('seiko_favorite_blog.urls')),
    path('comment/', include('comment.urls')),
    path('ckeditor', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    # add root static files
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # add media static files
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
