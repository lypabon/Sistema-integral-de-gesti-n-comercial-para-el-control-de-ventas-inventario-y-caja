"""Capa de lógica de negocio del módulo Gestión de Inventario.

Todo cambio de stock pasa por aquí y deja un MovimientoInventario.
"""
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F

from apps.productos.models import Producto

from .models import Existencia, MovimientoInventario


class StockInsuficiente(ValidationError):
    pass


def _existencia_bloqueada(producto):
    """Obtiene la existencia bloqueando la fila para evitar ventas simultáneas del mismo stock."""
    Existencia.objects.get_or_create(producto=producto)
    return Existencia.objects.select_for_update().get(producto=producto)


def stock_de(producto):
    existencia = Existencia.objects.filter(producto=producto).first()
    return existencia.cantidad if existencia else 0


def _validar_cantidad(cantidad):
    if cantidad is None or int(cantidad) <= 0:
        raise ValidationError("La cantidad debe ser mayor que cero.")


# IN-01 Registrar entrada de inventario
@transaction.atomic
def registrar_entrada(producto, cantidad, *, motivo, usuario=None, referencia=""):
    _validar_cantidad(cantidad)
    existencia = _existencia_bloqueada(producto)
    existencia.cantidad += cantidad
    existencia.save(update_fields=["cantidad"])
    return MovimientoInventario.objects.create(
        producto=producto, tipo=MovimientoInventario.Tipo.ENTRADA, cantidad=cantidad,
        stock_resultante=existencia.cantidad, motivo=motivo, referencia=referencia, usuario=usuario,
    )


# IN-02 Registrar salida de inventario
@transaction.atomic
def registrar_salida(producto, cantidad, *, motivo, usuario=None, referencia=""):
    _validar_cantidad(cantidad)
    existencia = _existencia_bloqueada(producto)
    if existencia.cantidad < cantidad:
        raise StockInsuficiente(
            f"Stock insuficiente de {producto.nombre}: hay {existencia.cantidad} y se piden {cantidad}."
        )
    existencia.cantidad -= cantidad
    existencia.save(update_fields=["cantidad"])
    return MovimientoInventario.objects.create(
        producto=producto, tipo=MovimientoInventario.Tipo.SALIDA, cantidad=-cantidad,
        stock_resultante=existencia.cantidad, motivo=motivo, referencia=referencia, usuario=usuario,
    )


# IN-03 Ajustar inventario
@transaction.atomic
def ajustar_inventario(producto, conteo_fisico, *, motivo, usuario=None):
    if conteo_fisico is None or int(conteo_fisico) < 0:
        raise ValidationError("El conteo físico no puede ser negativo.")
    if not motivo or not motivo.strip():
        raise ValidationError("Todo ajuste de inventario debe tener un motivo.")
    existencia = _existencia_bloqueada(producto)
    diferencia = conteo_fisico - existencia.cantidad
    if diferencia == 0:
        return None
    existencia.cantidad = conteo_fisico
    existencia.save(update_fields=["cantidad"])
    return MovimientoInventario.objects.create(
        producto=producto, tipo=MovimientoInventario.Tipo.AJUSTE, cantidad=diferencia,
        stock_resultante=conteo_fisico, motivo=motivo.strip(), usuario=usuario,
    )


# IN-04 Generar alertas de bajo stock
def productos_bajo_stock():
    """Productos activos cuyo stock es igual o menor a su stock mínimo (incluye los que nunca han tenido stock)."""
    con_existencia = (
        Producto.objects.filter(activo=True, existencia__isnull=False)
        .filter(existencia__cantidad__lte=F("stock_minimo"))
    )
    sin_existencia = Producto.objects.filter(activo=True, existencia__isnull=True)
    return (con_existencia | sin_existencia).select_related("categoria").distinct().order_by("nombre")
