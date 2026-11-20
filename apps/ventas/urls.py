from django.urls import path

from . import views

app_name = "ventas"

urlpatterns = [
    path("", views.lista, name="lista"),
    path("nueva/", views.nueva_venta, name="nueva"),
    path("<int:pk>/comprobante/", views.comprobante, name="comprobante"),
]
