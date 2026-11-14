from django.urls import path

from . import views

app_name = "productos"

urlpatterns = [
    path("", views.lista_productos, name="lista"),
    path("nuevo/", views.crear_producto, name="crear"),
    path("<int:pk>/editar/", views.editar_producto, name="editar"),
    path("<int:pk>/estado/", views.cambiar_estado, name="estado"),
    path("<int:pk>/precio/", views.cambiar_precio, name="precio"),
    path("categorias/", views.categorias, name="categorias"),
    path("categorias/<int:pk>/eliminar/", views.eliminar_categoria, name="eliminar_categoria"),
]
