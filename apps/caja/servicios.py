"""Capa de lógica de negocio del módulo Caja.

Fórmula de cuadre (CJ-02):
    efectivo esperado = fondo inicial + ventas en efectivo + ingresos − egresos
    diferencia        = efectivo contado − efectivo esperado
"""
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone

from .models import Caja, MedioPago, MovimientoCaja

CERO = Decimal("0.00")


def caja_abierta_de(usuario):
    return Caja.objects.filter(responsable=usuario, estado=Caja.Estado.ABIERTA).first()


def _exigir_abierta(caja):
    if caja is None or caja.estado != Caja.Estado.ABIERTA:
        raise ValidationError("La caja no está abierta.")


def _validar_monto(monto, nombre="El monto"):
    if monto is None or Decimal(monto) <= 0:
        raise ValidationError(f"{nombre} debe ser mayor que cero.")


# CJ-01 Abrir caja
@transaction.atomic
def abrir_caja(usuario, fondo_inicial):
    if Decimal(fondo_inicial) < 0:
        raise ValidationError("El fondo inicial no puede ser negativo.")
    if caja_abierta_de(usuario):
        raise ValidationError("Ya tiene una caja abierta. Ciérrela antes de abrir otra.")
    return Caja.objects.create(responsable=usuario, fondo_inicial=fondo_inicial)


# CJ-03 Registrar ingresos y egresos
def registrar_movimiento(caja, tipo, monto, *, motivo, usuario=None):
    _exigir_abierta(caja)
    if tipo not in (MovimientoCaja.Tipo.INGRESO, MovimientoCaja.Tipo.EGRESO):
        raise ValidationError("Solo se registran a mano ingresos y egresos; las ventas entran solas.")
    _validar_monto(monto)
    if not motivo or not motivo.strip():
        raise ValidationError("Todo ingreso o egreso debe tener un motivo.")
    if tipo == MovimientoCaja.Tipo.EGRESO and Decimal(monto) > efectivo_esperado(caja):
        raise ValidationError("No hay suficiente efectivo en la caja para ese egreso.")
    return MovimientoCaja.objects.create(
        caja=caja, tipo=tipo, monto=monto, motivo=motivo.strip(), usuario=usuario,
        medio_pago=MedioPago.EFECTIVO,
    )


def registrar_cobro_de_venta(caja, monto, medio_pago, *, referencia, usuario=None):
    """Lo usa el módulo de Ventas (VE-04) al confirmar una venta."""
    _exigir_abierta(caja)
    _validar_monto(monto)
    return MovimientoCaja.objects.create(
        caja=caja, tipo=MovimientoCaja.Tipo.VENTA, monto=monto, medio_pago=medio_pago,
        motivo="Venta", referencia=referencia, usuario=usuario,
    )


def _suma(qs):
    return qs.aggregate(t=Sum("monto"))["t"] or CERO


def resumen(caja):
    movs = caja.movimientos.all()
    ventas = movs.filter(tipo=MovimientoCaja.Tipo.VENTA)
    return {
        "ventas_efectivo": _suma(ventas.filter(medio_pago=MedioPago.EFECTIVO)),
        "ventas_tarjeta": _suma(ventas.filter(medio_pago=MedioPago.TARJETA)),
        "ventas_transferencia": _suma(ventas.filter(medio_pago=MedioPago.TRANSFERENCIA)),
        "ingresos": _suma(movs.filter(tipo=MovimientoCaja.Tipo.INGRESO)),
        "egresos": _suma(movs.filter(tipo=MovimientoCaja.Tipo.EGRESO)),
    }


def efectivo_esperado(caja):
    r = resumen(caja)
    return caja.fondo_inicial + r["ventas_efectivo"] + r["ingresos"] - r["egresos"]


# CJ-02 Cerrar caja
@transaction.atomic
def cerrar_caja(caja, efectivo_contado, *, observacion="", usuario=None):
    _exigir_abierta(caja)
    if efectivo_contado is None or Decimal(efectivo_contado) < 0:
        raise ValidationError("Debe registrar el efectivo contado.")
    esperado = efectivo_esperado(caja)
    diferencia = Decimal(efectivo_contado) - esperado
    if diferencia != 0 and not (observacion and observacion.strip()):
        raise ValidationError(f"Hay un descuadre de {diferencia}. Escriba la explicación antes de cerrar.")
    caja.efectivo_esperado = esperado
    caja.efectivo_contado = efectivo_contado
    caja.diferencia = diferencia
    caja.observacion = (observacion or "").strip()
    caja.estado = Caja.Estado.CERRADA
    caja.cerrada_en = timezone.now()
    caja.save()
    return caja
