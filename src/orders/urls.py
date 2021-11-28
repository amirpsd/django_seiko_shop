from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("create/", views.order_create, name="create"),
    path("payment/<int:order_id>/<price>/", views.payment, name="payment"),
    path("verify/", views.verify, name="verify"),
]
