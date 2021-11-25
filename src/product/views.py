from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from .filters import ProductFilter
from .models import (
    Product,
    Category,
    CategoryImage,
    Slider,
)

from product.forms import Paginate_by_form
from cart.forms import CartAddProductForm

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


def category_list(request, slug):
    category = get_object_or_404(Category.objects.active(), slug=slug)
    category_list = category.category.publish()
    # or
    # product = Product.objects.publish().filter(category=category)

    paginator = Paginator(category_list, 8)

    form = Paginate_by_form(request.POST or None)
    if form.is_valid():
        page = form.cleaned_data.get("pagination")
        paginator = Paginator(category_list, page)

    page_number = request.GET.get("page")
    category_list = paginator.get_page(page_number)

    context = {
        "category": category,
        "object_list": category_list,
        "form": Paginate_by_form,
        "paginator": paginator,
    }

    return render(request, "main/category.html", context=context)


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
