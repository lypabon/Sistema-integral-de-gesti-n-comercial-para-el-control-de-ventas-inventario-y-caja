from django.urls import path

from . import views

app_name = "caja"

urlpatterns = [
    path("", views.mi_caja, name="mi_caja"),
    path("movimiento/", views.movimiento, name="movimiento"),
    path("cerrar/", views.cerrar, name="cerrar"),
    path("historial/", views.historial, name="historial"),
    path("<int:pk>/", views.detalle, name="detalle"),
]
