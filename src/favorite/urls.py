from django.urls import path

from .views import (
    favorite_product_list, favorite_product_add, favorite_product_remove,
    favorite_blog_list, favorite_blog_add, favorite_blog_remove,
)

app_name = "favorite"

urlpatterns = [
    # product
    path("product/", favorite_product_list, name="product-list"),
    path("product/add/<int:product_id>/", favorite_product_add, name="product-add"),
    path("product/remove/<int:product_id>/", favorite_product_remove, name="product-remove"),

    # blog
    path("blog/", favorite_blog_list, name="blog-list"),
    path("blog/add/<int:blog_id>/", favorite_blog_add, name="blog-add"),
    path("blog/remove/<int:blog_id>/", favorite_blog_remove, name="blog-remove"),
]
