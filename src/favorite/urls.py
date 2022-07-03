from django.urls import path

from .views import (
    FavoriteProductList, favorite_product_add, favorite_product_remove,
    FavoriteBlogList, favorite_blog_add, favorite_blog_remove,
)

app_name = "favorite"

urlpatterns = [
    # product
    path("product/", FavoriteProductList.as_view(), name="product-list"),
    path("product/add/<int:product_id>/", favorite_product_add, name="product-add"),
    path("product/remove/<int:product_id>/", favorite_product_remove, name="product-remove"),

    # blog
    path("blog/", FavoriteBlogList.as_view(), name="blog-list"),
    path("blog/add/<int:blog_id>/", favorite_blog_add, name="blog-add"),
    path("blog/remove/<int:blog_id>/", favorite_blog_remove, name="blog-remove"),
]
