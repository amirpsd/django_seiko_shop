from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from django.views.generic import UpdateView
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render

from .tokens import account_activation_token
from .forms import SignupForm, ProfileForm
from .models import User


# Create your views here


class Profile(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "account_panel/index.html"
    success_url = reverse_lazy("account:profile")

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = _("Active your account")
            message = render_to_string(
                "registration/acc_active_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            to_email = form.cleaned_data.get("email")
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse(_("Please confirm your email address to complete registration"))
    else:
        form = SignupForm()
    return render(request, "registration/account-create.html", {"form": form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return HttpResponse(
            _("Thank you for verifying your email. You can now enter your account.")
        )
    else:
        return HttpResponse(_("The activation link is invalid!"))
