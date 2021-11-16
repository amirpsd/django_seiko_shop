from django.urls import path

from .views import (
    favorite_blog_list,
    favorite_blog_add,
    favorite_blog_remove,
)

app_name = "favorite-blog"

urlpatterns = [
    path("", favorite_blog_list, name="list"),
    path("<int:blog_id>", favorite_blog_add, name="add"),
    path("remove/<int:blog_id>", favorite_blog_remove, name="remove"),
]
