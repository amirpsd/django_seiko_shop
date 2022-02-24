from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

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


@login_required
def favorite_product_list(request):
    favorite_product = FavoriteProduct.objects.filter(user=request.user)
    context = {"favorite": favorite_product}
    return render(request, "account_panel/favoriteproduct.html", context)


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


@login_required
def favorite_blog_list(request):
    favorite_list = FavoriteBlog.objects.filter(user=request.user)
    context = {"favorite_list": favorite_list}
    return render(request, "account_panel/favoriteblog.html", context)


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
