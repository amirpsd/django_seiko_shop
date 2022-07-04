from django import forms

import django_filters

from .models import Color, Size, Product, Category


class ProductFilter(django_filters.FilterSet):
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name="price", lookup_expr="gt")
    price__lt = django_filters.NumberFilter(field_name="price", lookup_expr="lt")
    colors = django_filters.ModelMultipleChoiceFilter(
        queryset=Color.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    sizes = django_filters.ModelMultipleChoiceFilter(
        queryset=Size.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.active(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        Model = Product.objects.publish()
        fields = {
            "price": ["lt", "gt"],
        }
