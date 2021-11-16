from django.urls import path

from .views import (
    BlogList,
    DetailBlog,
    CategoryBlog,
)


app_name = "blog"

urlpatterns = [
    path("", BlogList.as_view(), name="list"),
    path("<slug:slug>/", DetailBlog.as_view(), name="detail"),
    path("category/<slug:slug>", CategoryBlog.as_view(), name="category"),
]
