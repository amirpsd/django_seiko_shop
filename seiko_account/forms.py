from django.contrib.auth.forms import UserCreationForm
from django import forms

from captcha.fields import ReCaptchaField
from .models import User


class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ProfileForm, self).__init__(*args, **kwargs)
        if not user.is_superuser:
            self.fields['username'].disabled = True
            self.fields['username'].help_text = None
            self.fields['email'].disabled = True

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']


class SignupForm(UserCreationForm):
    captcha = ReCaptchaField()
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
