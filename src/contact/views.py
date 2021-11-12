from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import ContactForm
from .models import Contact


# Create your views here.


class ContactHome(CreateView):
    model = Contact
    form_class = ContactForm
    success_url = reverse_lazy("seiko:home")
    template_name = 'main/contact.html'
