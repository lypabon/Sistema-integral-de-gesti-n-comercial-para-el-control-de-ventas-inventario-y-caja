"""Capa de persistencia del módulo Caja (CJ-01 a CJ-03)."""
from django.conf import settings
from django.db import models


class MedioPago(models.TextChoices):
    EFECTIVO = "EFECTIVO", "Efectivo"
    TARJETA = "TARJETA", "Tarjeta"
    TRANSFERENCIA = "TRANSFERENCIA", "Transferencia"


class Caja(models.Model):
    """Turno de caja de un usuario, desde la apertura hasta el cierre."""

    class Estado(models.TextChoices):
        ABIERTA = "ABIERTA", "Abierta"
        CERRADA = "CERRADA", "Cerrada"

    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="cajas")
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.ABIERTA)
    fondo_inicial = models.DecimalField(max_digits=12, decimal_places=2)
    abierta_en = models.DateTimeField(auto_now_add=True)
    cerrada_en = models.DateTimeField(null=True, blank=True)
    efectivo_esperado = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    efectivo_contado = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    diferencia = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    observacion = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ["-abierta_en", "-id"]

    def __str__(self):
        return f"Caja #{self.pk} de {self.responsable} ({self.get_estado_display()})"


class MovimientoCaja(models.Model):
    """Ventas cobradas, ingresos y egresos de un turno de caja."""

    class Tipo(models.TextChoices):
        VENTA = "VENTA", "Venta"
        INGRESO = "INGRESO", "Ingreso"
        EGRESO = "EGRESO", "Egreso"

    caja = models.ForeignKey(Caja, on_delete=models.PROTECT, related_name="movimientos")
    tipo = models.CharField(max_length=10, choices=Tipo.choices)
    medio_pago = models.CharField(max_length=15, choices=MedioPago.choices, default=MedioPago.EFECTIVO)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    motivo = models.CharField(max_length=200)
    referencia = models.CharField(max_length=50, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["fecha", "id"]
        verbose_name = "movimiento de caja"
        verbose_name_plural = "movimientos de caja"

    def __str__(self):
        return f"{self.get_tipo_display()} {self.monto} ({self.get_medio_pago_display()})"
