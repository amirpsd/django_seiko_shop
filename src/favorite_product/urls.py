from django.urls import path

from .views import (
    favorite_product_list,
    favorite_product_add,
    favorite_product_remove,
)

app_name = "favorite-product"

urlpatterns = [
    path("", favorite_product_list, name="list"),
    path("<int:product_id>/", favorite_product_add, name="add"),
    path("remove/<int:product_id>/", favorite_product_remove, name="remove"),
]
