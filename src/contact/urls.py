from django.urls import path
from .views import ContactHome

app_name = "contact"

urlpatterns = [
    path("", ContactHome.as_view(), name="home"),
]
