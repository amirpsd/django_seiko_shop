from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import FavoriteBlog
from blog.models import Blog


# Create your views here.


@login_required
def favorite_blog_list(request):
    favorite_list = FavoriteBlog.objects.filter(user=request.user)
    context = {"favorite_list": favorite_list}
    return render(request, "account_panel/favoriteblog.html", context)


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

    return redirect("favorite-blog:list")


@login_required
def favorite_blog_remove(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    favorite = FavoriteBlog.objects.get(user=request.user)
    favorite.blogs.remove(blog)
    if not favorite.blogs.all().exists():
        favorite.delete()

    return redirect("favorite-blog:list")
