"""Capa de persistencia del módulo Gestión de Inventario (IN-01 a IN-04)."""
from django.conf import settings
from django.db import models

from apps.productos.models import Producto


class Existencia(models.Model):
    """Stock actual de un producto. Solo se modifica a través de los servicios."""

    producto = models.OneToOneField(Producto, on_delete=models.CASCADE, related_name="existencia")
    cantidad = models.IntegerField(default=0)

    class Meta:
        verbose_name = "existencia"

    def __str__(self):
        return f"{self.producto.codigo}: {self.cantidad}"


class MovimientoInventario(models.Model):
    """Registro inalterable de cada entrada, salida o ajuste de stock."""

    class Tipo(models.TextChoices):
        ENTRADA = "ENTRADA", "Entrada"
        SALIDA = "SALIDA", "Salida"
        AJUSTE = "AJUSTE", "Ajuste"

    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name="movimientos")
    tipo = models.CharField(max_length=10, choices=Tipo.choices)
    cantidad = models.IntegerField(help_text="Positiva suma stock, negativa resta stock.")
    stock_resultante = models.IntegerField()
    motivo = models.CharField(max_length=200)
    referencia = models.CharField(max_length=50, blank=True, help_text="Por ejemplo, el número de la venta o de la compra.")
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["-fecha", "-id"]
        verbose_name = "movimiento de inventario"
        verbose_name_plural = "movimientos de inventario"

    def __str__(self):
        return f"{self.get_tipo_display()} {self.cantidad:+d} {self.producto.codigo}"
