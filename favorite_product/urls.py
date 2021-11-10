from django.urls import path

from .views import (
    favorite_add_product,
    favoritelistview,
    favorite_remove_product,
)

app_name = 'favorite'
urlpatterns = [
    path('', favoritelistview, name='list'),
    path('<int:product_id>/', favorite_add_product, name='add'),
    path('remove/<int:product_id>/', favorite_remove_product, name='remove'),
]
