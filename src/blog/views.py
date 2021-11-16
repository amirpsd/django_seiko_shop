from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404

from .models import Blog, Category


# Create your views here.


class BlogList(ListView):
    template_name = "main/blog.html"
    paginate_by = 10

    def get_queryset(self):
        blog = Blog.objects.get_published_post()
        return blog.order_by("-publish")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.active()
        return context


class DetailBlog(DetailView):
    template_name = "main/blog-single.html"
    context_object_name = "blog"

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        detail_blog = get_object_or_404(Blog, status="p", slug=slug)
        return detail_blog


class CategoryBlog(ListView):
    template_name = "main/categoryblog.html"
    paginate_by = 8

    def get_queryset(self):
        global category  # noqa
        slug = self.kwargs.get("slug")
        category = get_object_or_404(Category, status=True, slug=slug)
        return category.blog_category.get_published_post()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = category
        return context
