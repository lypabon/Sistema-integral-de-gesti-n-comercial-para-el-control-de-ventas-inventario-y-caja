"""Capa de persistencia del módulo Gestión de Productos (PR-01 a PR-04)."""
from django.conf import settings
from django.db import models


class Categoria(models.Model):
    """PR-03: clasificación del catálogo."""

    nombre = models.CharField(max_length=80, unique=True)
    descripcion = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "categoría"

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    """PR-01 y PR-02: artículo del catálogo. No se borra: se inactiva."""

    codigo = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=120)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="productos")
    precio_venta = models.DecimalField(max_digits=12, decimal_places=2)
    stock_minimo = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class HistorialPrecio(models.Model):
    """PR-04: trazabilidad de cada cambio de precio de venta."""

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="historial_precios")
    precio_anterior = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    precio_nuevo = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["-fecha", "-id"]
        verbose_name = "historial de precio"
        verbose_name_plural = "historial de precios"

    def __str__(self):
        return f"{self.producto.codigo}: {self.precio_anterior} -> {self.precio_nuevo}"
