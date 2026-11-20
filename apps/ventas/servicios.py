"""Capa de lógica de negocio del módulo Gestión de Ventas.

Una venta se confirma completa o no se confirma: el registro de la venta,
la salida de inventario de cada producto y el cobro en la caja se guardan
en una sola transacción (control del proceso PN-04).

Reglas de cálculo (VE-02):
    subtotal  = Σ cantidad × precio de venta
    descuento = subtotal × % descuento        (máximo VENTAS_DESCUENTO_MAX)
    impuesto  = (subtotal − descuento) × VENTAS_IVA
    total     = subtotal − descuento + impuesto
"""
from collections import OrderedDict
from decimal import ROUND_HALF_UP, Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction

from apps.caja import servicios as caja_srv
from apps.caja.models import MedioPago
from apps.inventario import servicios as inv_srv

from .models import DetalleVenta, Venta

CENTAVO = Decimal("0.01")


def _redondear(valor):
    return Decimal(valor).quantize(CENTAVO, rounding=ROUND_HALF_UP)


def iva():
    return Decimal(str(getattr(settings, "VENTAS_IVA", "0.19")))


def descuento_maximo():
    return Decimal(str(getattr(settings, "VENTAS_DESCUENTO_MAX", "10")))


# VE-02 Aplicar descuentos e impuestos
def calcular_totales(lineas, descuento_pct=0):
    """lineas: lista de (producto, cantidad). Devuelve el desglose de la venta."""
    descuento_pct = Decimal(str(descuento_pct or 0))
    if descuento_pct < 0 or descuento_pct > descuento_maximo():
        raise ValidationError(f"El descuento debe estar entre 0 % y {descuento_maximo()} %.")
    subtotal = sum((p.precio_venta * c for p, c in lineas), Decimal("0"))
    subtotal = _redondear(subtotal)
    descuento = _redondear(subtotal * descuento_pct / 100)
    impuesto = _redondear((subtotal - descuento) * iva())
    total = subtotal - descuento + impuesto
    return {"subtotal": subtotal, "descuento_pct": descuento_pct, "descuento": descuento, "impuesto": impuesto, "total": total}


def _agrupar(lineas):
    """Une líneas repetidas del mismo producto y valida cantidades."""
    agrupadas = OrderedDict()
    for producto, cantidad in lineas:
        if cantidad is None or int(cantidad) <= 0:
            raise ValidationError("Cada producto debe tener una cantidad mayor que cero.")
        if not producto.activo:
            raise ValidationError(f"{producto.nombre} está inactivo y no se puede vender.")
        agrupadas[producto] = agrupadas.get(producto, 0) + int(cantidad)
    if not agrupadas:
        raise ValidationError("La venta debe tener al menos un producto.")
    return list(agrupadas.items())


def _siguiente_numero():
    ultima = Venta.objects.select_for_update().order_by("-id").first()
    siguiente = (int(ultima.numero.split("-")[1]) + 1) if ultima else 1
    return f"V-{siguiente:06d}"


# VE-01 Crear venta · VE-03 Comprobante · VE-04 Medio de pago
@transaction.atomic
def registrar_venta(vendedor, lineas, *, medio_pago, monto_recibido=None, descuento_pct=0):
    caja = caja_srv.caja_abierta_de(vendedor)
    if caja is None:
        raise ValidationError("Debe abrir la caja antes de vender.")
    if medio_pago not in MedioPago.values:
        raise ValidationError("Medio de pago no válido.")

    lineas = _agrupar(lineas)
    totales = calcular_totales(lineas, descuento_pct)

    if medio_pago == MedioPago.EFECTIVO:
        if monto_recibido is None or Decimal(monto_recibido) < totales["total"]:
            raise ValidationError(f"El efectivo recibido no alcanza para pagar {totales['total']}.")
        monto_recibido = _redondear(monto_recibido)
    else:
        monto_recibido = totales["total"]

    numero = _siguiente_numero()
    venta = Venta.objects.create(
        numero=numero, caja=caja, vendedor=vendedor, medio_pago=medio_pago,
        monto_recibido=monto_recibido, cambio=monto_recibido - totales["total"], **totales,
    )
    for producto, cantidad in lineas:
        # Si falta stock, se lanza StockInsuficiente y toda la venta se deshace.
        inv_srv.registrar_salida(producto, cantidad, motivo="Venta", usuario=vendedor, referencia=numero)
        DetalleVenta.objects.create(
            venta=venta, producto=producto, cantidad=cantidad,
            precio_unitario=producto.precio_venta, subtotal=_redondear(producto.precio_venta * cantidad),
        )
    caja_srv.registrar_cobro_de_venta(caja, totales["total"], medio_pago, referencia=numero, usuario=vendedor)
    return venta
