"""Capa de persistencia del módulo Gestión de Ventas (VE-01 a VE-04)."""
from django.conf import settings
from django.db import models

from apps.caja.models import Caja, MedioPago
from apps.productos.models import Producto


class Venta(models.Model):
    numero = models.CharField(max_length=20, unique=True, help_text="Número del comprobante (VE-03).")
    caja = models.ForeignKey(Caja, on_delete=models.PROTECT, related_name="ventas")
    vendedor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="ventas")
    fecha = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    descuento_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2)
    impuesto = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    medio_pago = models.CharField(max_length=15, choices=MedioPago.choices)
    monto_recibido = models.DecimalField(max_digits=12, decimal_places=2)
    cambio = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ["-fecha", "-id"]

    def __str__(self):
        return f"{self.numero} · {self.total}"


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
