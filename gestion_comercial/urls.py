from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from apps.usuarios.views import inicio

urlpatterns = [
    path("", inicio, name="inicio"),
    path("ingresar/", auth_views.LoginView.as_view(template_name="ingresar.html"), name="login"),
    path("salir/", auth_views.LogoutView.as_view(), name="logout"),
    path("usuarios/", include("apps.usuarios.urls")),
    path("productos/", include("apps.productos.urls")),
    path("inventario/", include("apps.inventario.urls")),
    path("caja/", include("apps.caja.urls")),
    path("ventas/", include("apps.ventas.urls")),
    path("admin/", admin.site.urls),
]
