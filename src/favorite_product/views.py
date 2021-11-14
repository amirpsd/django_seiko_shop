from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required

from .models import FavoriteProduct
from product.models import Product


# Create your views here.


@login_required
def favorite_product_add(request, product_id):
    product = get_object_or_404(Product, status='pub', id=product_id)
    favorite, created = FavoriteProduct.objects.get_or_create(user=request.user)

    if product in favorite.products.all():
        favorite.products.remove(product)
    else:
        favorite.products.add(product)
    if not favorite.products.all().exists():
        favorite.delete()


    return redirect('favorite-product:list')


@login_required
def favorite_product_list(request):
    favorite_product = FavoriteProduct.objects.filter(user=request.user)
    favorite_product.all()
    context = {
        'favorite': favorite_product
    }
    return render(request, 'account_panel/favoriteproduct.html', context)


@login_required
def favorite_product_remove(request, product_id):
    product = get_object_or_404(Product, status='pub', id=product_id)
    favorite_remove = FavoriteProduct.objects.get(user=request.user)
    favorite_remove.products.remove(product)
    if not favorite_remove.products.all().exists():
        favorite_remove.delete()

    return redirect('favorite-product:list')
