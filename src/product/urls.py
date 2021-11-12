from django.urls import path

from .views import (
    ProductList,
    SearchProduct,
    ProductDetail,
    CategoryList,
    about_us,
)


app_name = 'product'

urlpatterns = [
    path('', ProductList.as_view(), name='home'),
    path('category/<slug:slug>/', CategoryList.as_view(), name='category'),
    path('products/<slug:slug>/<int:id>',
         ProductDetail.as_view(), name='detail'),
    path('products/search/', SearchProduct.as_view(), name='search'),
    path('about-us/', about_us, name='about'),
]
