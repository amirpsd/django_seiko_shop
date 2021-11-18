from product.models import Product
from blog.models import Blog


def product_special_offer(request):
    product = Product.objects.filter(special_offer=True, status="pub").order_by(
        "-publish"
    )[:4]

    return {
        "product_special_offer": product,
    }


def suggested_blog(request):
    blog = Blog.objects.get_published_post().order_by("-publish")[:4]

    return {
        "suggested_blog": blog,
    }
