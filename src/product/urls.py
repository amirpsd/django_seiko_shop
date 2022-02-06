from django.views.generic import TemplateView
from django.urls import path

from .views import (
    ProductList,
    SearchProduct,
    ProductDetail,
    category_list,
    comment_delete,
)


app_name = "product"

urlpatterns = [
    path("", ProductList.as_view(), name="home"),
    path("products/comment-delete/<int:comment_id>/", comment_delete, name="comment-delete"),
    path("category/<slug:slug>/", category_list, name="category"),
    path("products/<slug:slug>/<int:id>/", ProductDetail.as_view(), name="detail"),
    path("products/search/", SearchProduct.as_view(), name="search"),
    path("about-us/", TemplateView.as_view(template_name="main/about.html"), name="about"),
]
