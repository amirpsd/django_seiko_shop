from django.forms import ModelForm
from django.core.validators import ValidationError

from captcha.fields import ReCaptchaField  # noqa
from validate_email import validate_email  # noqa

from .models import Contact


class ContactForm(ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Contact
        fields = ['name', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        is_valid = validate_email(
            email_address=email,
            check_format=True,
            check_blacklist=True,
            check_dns=True,
            dns_timeout=10,
            check_smtp=True,
            smtp_timeout=10,
            smtp_helo_host='localhost',
            smtp_skip_tls=False,
            smtp_tls_context=None,
            smtp_debug=False
        )

        if not is_valid:
            raise ValidationError(message='ایمیل معتبر نیست لطفا ایمیل دیگری را امتحان کنید')
        return email
