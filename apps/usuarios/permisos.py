"""Control de acceso por roles (US-02).

Matriz de permisos acordada en el diseño:
- Administrador: todo el sistema.
- Vendedor: ventas, clientes, caja y consulta de productos.
- Encargado de bodega: productos, inventario y compras.
"""
from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import Rol

PERMISOS = {
    "productos.consultar": {Rol.ADMINISTRADOR, Rol.VENDEDOR, Rol.BODEGA},
    "productos.gestionar": {Rol.ADMINISTRADOR, Rol.BODEGA},
    "productos.precios": {Rol.ADMINISTRADOR},
    "inventario.gestionar": {Rol.ADMINISTRADOR, Rol.BODEGA},
    "compras.gestionar": {Rol.ADMINISTRADOR, Rol.BODEGA},
    "ventas.registrar": {Rol.ADMINISTRADOR, Rol.VENDEDOR},
    "clientes.gestionar": {Rol.ADMINISTRADOR, Rol.VENDEDOR},
    "caja.operar": {Rol.ADMINISTRADOR, Rol.VENDEDOR},
    "reportes.consultar": {Rol.ADMINISTRADOR},
    "usuarios.gestionar": {Rol.ADMINISTRADOR},
}


def puede(usuario, permiso):
    """Indica si el usuario tiene el permiso indicado."""
    if not usuario.is_authenticated:
        return False
    if usuario.is_superuser:
        return True
    return usuario.rol in PERMISOS.get(permiso, set())


def permiso_requerido(permiso):
    """Decorador para vistas: exige sesión iniciada y el permiso indicado."""

    def decorador(vista):
        @wraps(vista)
        @login_required
        def envoltura(request, *args, **kwargs):
            if not puede(request.user, permiso):
                raise PermissionDenied("No tiene permiso para esta acción.")
            return vista(request, *args, **kwargs)

        return envoltura

    return decorador
