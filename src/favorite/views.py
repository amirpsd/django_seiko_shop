from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.views.generic import ListView

from .models import FavoriteProduct, FavoriteBlog
from product.models import Product
from blog.models import Blog


# Create your views here.

@csrf_exempt
@require_GET
@login_required
def favorite_product_add(request, product_id):
    product = get_object_or_404(Product, status="a", id=product_id)
    favorite, created = FavoriteProduct.objects.get_or_create(user=request.user)

    if product in favorite.products.all():
        favorite.products.remove(product)
    else:
        favorite.products.add(product)
    if not favorite.products.all().exists():
        favorite.delete()

    return redirect("favorite:product-list")


class FavoriteProductList(LoginRequiredMixin, ListView):
    template_name = "account_panel/favoriteproduct.html"
    paginate_by = 24

    def get_queryset(self):
        favorite_product = FavoriteProduct.objects.filter(user=self.request.user)
        if favorite_product:
            return favorite_product.first().products.all()
        return favorite_product
    

@csrf_exempt
@require_GET
@login_required
def favorite_product_remove(request, product_id):
    product = get_object_or_404(Product, status="a", id=product_id)
    favorite_remove = FavoriteProduct.objects.get(user=request.user)
    favorite_remove.products.remove(product)
    if not favorite_remove.products.all().exists():
        favorite_remove.delete()

    return redirect("favorite:product-list")


@csrf_exempt
@require_GET
@login_required
def favorite_blog_add(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    favorite, created = FavoriteBlog.objects.get_or_create(user=request.user)

    if blog in favorite.blogs.all():
        favorite.blogs.remove(blog)
    else:
        favorite.blogs.add(blog)
    if not favorite.blogs.all().exists():
        favorite.delete()

    return redirect("favorite:blog-list")


class FavoriteBlogList(LoginRequiredMixin, ListView):
    template_name = "account_panel/favoriteblog.html"
    paginate_by = 1

    def get_queryset(self):
        favorite_blog = FavoriteBlog.objects.filter(user=self.request.user)
        if favorite_blog:
            return favorite_blog.first().blogs.all()
        return favorite_blog


@csrf_exempt
@require_GET
@login_required
def favorite_blog_remove(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    favorite = FavoriteBlog.objects.get(user=request.user)
    favorite.blogs.remove(blog)
    if not favorite.blogs.all().exists():
        favorite.delete()

    return redirect("favorite:blog-list")
