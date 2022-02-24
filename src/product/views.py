from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q

from .filters import ProductFilter
from .models import (
    Product,
    Category,
    Comment,
    Slider,
)

from product.forms import Paginate_by_form, CommentForm
from cart.forms import CartAddProductForm

###############

# Create your views here.


class ProductList(ListView):
    template_name = "main/index-rtl.html"
    paginate_by = 24

    def get_queryset(self):
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
        global product
        product = Product.objects.publish()
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
    category_list = category.products.publish()
    # or
    # product = Product.objects.publish().filter(category=category)

    page = request.GET.get("pagination")
    if page:
        paginator = Paginator(category_list, page)
    else:
        paginator = Paginator(category_list, 8)

    page_number = request.GET.get("page")
    category_list = paginator.get_page(page_number)

    context = {
        "category": category,
        "object_list": category_list,
        "form": Paginate_by_form,
        "paginator": paginator,
    }

    return render(request, "main/category.html", context=context)


class ProductDetail(FormMixin, DetailView):
    template_name = "main/product.html"
    context_object_name = "product"
    form_class = CommentForm

    def get_success_url(self):
        return reverse(
            "product:detail", kwargs={"slug": self.object.slug, "id": self.object.id}
        )

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        id = self.kwargs.get("id")
        product_detail = get_object_or_404(Product, slug=slug, id=id, status="a")
        return product_detail

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart_product_form"] = CartAddProductForm(
            initial={
                "color":self.object.colors.all(),
                "size":self.object.sizes.all(),
            }
        )
        context["comment_form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            try:
                myform = form.save(commit=False)
                myform.user = self.request.user
                myform.product = self.object
                myform.save()
            except:
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    "شما نمیتوانید در یک روز بیش از یک نظر بگذارید",
                )
        else:
            messages.add_message(
                self.request,
                messages.ERROR,
                "برای افزودن نظر باید وارد شوید",
            )       

        return super(ProductDetail, self).form_valid(form)


def comment_delete(request, comment_id):
    comment = get_object_or_404(
        Comment, 
        user=request.user, 
        id=comment_id
    )
    slug = comment.product.slug
    id = comment.product.id
    comment.delete()
    return redirect(reverse("product:detail", args=[slug, id]))

