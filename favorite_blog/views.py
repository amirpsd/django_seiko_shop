from django.shortcuts import render, get_object_or_404, redirect
from .models import FavoriteBlog
from django.contrib.auth.decorators import login_required
from blog.models import Blog


# Create your views here.

@login_required
def favorite_blog_list(request):
    favorite_list = FavoriteBlog.objects.filter(user=request.user)
    context = {
        "favorite_list": favorite_list
    }
    return render(request, 'account_panel/favoriteblog.html', context)


@login_required
def favorite_blog_add(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    favorite, created = FavoriteBlog.objects.get_or_create(user=request.user)
    try:
        favorite.blog.get(id=blog)
    except TypeError:
        favorite.blog.add(blog) 

    return redirect('/blog')


@login_required
def favorite_blog_remove(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    favorite = FavoriteBlog.objects.get(user=request.user)
    favorite.blog.remove(blog)
    if not favorite.blog.all().exists():
        favorite.delete()

    return redirect('/account/favorite/blog')
