from django import forms
from .models import Order

### create forms


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["full_name", "address", "postal_code", "city"]
