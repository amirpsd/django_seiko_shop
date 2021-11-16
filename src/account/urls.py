# The views used below are normally mapped in the AdminSite instance.
# This URLs file is used to provide a reliable view deployment for test purposes.
# It is also provided as a convenience to those who want to deploy these URLs
# elsewhere.

from django.urls import path
from .views import Profile, signup, activate

app_name = "account"
urlpatterns = [
    path("profile/", Profile.as_view(), name="profile"),
    path("signup/", signup, name="signup"),
    path("activate/<uidb64>/<token>/", activate, name="activate"),
]
