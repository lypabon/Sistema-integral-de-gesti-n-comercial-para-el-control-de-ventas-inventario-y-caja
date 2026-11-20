from django.urls import path

from . import views

app_name = "inventario"

urlpatterns = [
    path("", views.existencias, name="existencias"),
    path("entrada/", views.entrada, name="entrada"),
    path("ajuste/", views.ajuste, name="ajuste"),
    path("movimientos/", views.movimientos, name="movimientos"),
]
