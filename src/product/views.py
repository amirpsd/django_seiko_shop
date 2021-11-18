from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from .filters import ProductFilter
from .models import (
    Product,
    Category,
    CategoryImage,
    Slider,
)

from cart.forms import CartAddProductForm
from blog.models import Blog


###############

# Create your views here.


class ProductList(ListView):
    template_name = "main/index-rtl.html"
    paginate_by = 24

    def get_queryset(self):
        global product  # noqa
        product = Product.objects.publish()
        return product.order_by("-price", "-publish")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["slider"] = Slider.objects.all()
        return context


class SearchProduct(ListView):
    template_name = "main/search.html"
    paginate_by = 16

    def get_queryset(self):
        search = self.request.GET.get("q")
        if search is not None:
            return (
                product.filter(
                    Q(title__icontains=search)
                    | Q(description__icontains=search)
                    | Q(category__title__icontains=search)
                )
                .distinct()
                .order_by("-publish")
            )
        else:
            return product.order_by("-publish")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search"] = self.request.GET.get("q")
        context["filter"] = ProductFilter(self.request.GET, queryset=product)
        return context


class CategoryList(ListView):
    template_name = "main/category.html"
    paginate_by = 8

    def get_queryset(self):
        global category  # noqa
        slug = self.kwargs.get("slug")
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.category.publish()
        #####  or
        # product = Product.objects.publish().filter(category=category)
        # return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = category
        context["categoryimage"] = CategoryImage.objects.filter(category=category)
        return context


class ProductDetail(DetailView):
    template_name = "main/product.html"
    context_object_name = "product"

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        id = self.kwargs.get("id")  # noqa
        product_detail = get_object_or_404(product, slug=slug, id=id, status="pub")
        return product_detail

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart_product_form"] = CartAddProductForm()
        return context


def about_us(request):
    context = {}
    return render(request, "main/about.html", context)
