from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("create/", views.order_create, name="create"),
    path("pdf/<int:order_id>", views.render_order_pdf, name="pdf"),
]
