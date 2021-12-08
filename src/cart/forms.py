from django import forms

from product.models import Color

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 26)]


class CartAddProductForm(forms.Form):
    def __init__(self, *args, **kwargs):
    
        super(CartAddProductForm, self).__init__(*args, **kwargs)
        if kwargs:
            try:
                initial = kwargs.pop("initial")
                colors = initial.get('color')
                self.fields['color'].queryset = colors.all()
            except:
                pass
        if args:
            pass

    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label="تعداد"
    )
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    color = forms.ModelChoiceField(queryset=Color.objects.all())