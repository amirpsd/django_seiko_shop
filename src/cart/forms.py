from django import forms

from product.models import Color, Size

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 26)]


class CartAddProductForm(forms.Form):
    def __init__(self, *args, **kwargs):
    
        super(CartAddProductForm, self).__init__(*args, **kwargs)
        if kwargs:
            try:
                initial = kwargs.pop("initial")
                colors = initial.get('color')
                sizes = initial.get('size')
                self.fields['color'].queryset = colors.all()
                self.fields['size'].queryset = sizes.all()
            except:
                pass
        if args:
            pass

    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label="تعداد"
    )
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    color = forms.ModelChoiceField(queryset=Color.objects.all())
    size = forms.ModelChoiceField(queryset=Size.objects.all())