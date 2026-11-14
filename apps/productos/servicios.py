"""Capa de lógica de negocio del módulo Gestión de Productos.

Las vistas no tocan los modelos directamente: llaman a estas funciones,
que concentran las reglas de negocio y las validaciones.
"""
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Categoria, HistorialPrecio, Producto


def _validar_precio(precio):
    if precio is None or Decimal(precio) <= 0:
        raise ValidationError("El precio de venta debe ser mayor que cero.")


# PR-01 Registrar producto
@transaction.atomic
def registrar_producto(*, codigo, nombre, categoria, precio_venta, stock_minimo=0, usuario=None):
    codigo = codigo.strip().upper()
    if Producto.objects.filter(codigo__iexact=codigo).exists():
        raise ValidationError(f"Ya existe un producto con el código {codigo}.")
    _validar_precio(precio_venta)
    producto = Producto.objects.create(
        codigo=codigo,
        nombre=nombre.strip(),
        categoria=categoria,
        precio_venta=precio_venta,
        stock_minimo=stock_minimo,
    )
    HistorialPrecio.objects.create(producto=producto, precio_anterior=None, precio_nuevo=precio_venta, usuario=usuario)
    return producto


# PR-02 Editar / inactivar producto
def editar_producto(producto, *, nombre, categoria, stock_minimo):
    producto.nombre = nombre.strip()
    producto.categoria = categoria
    producto.stock_minimo = stock_minimo
    producto.save()
    return producto


def inactivar_producto(producto):
    """Se inactiva en lugar de borrar para conservar el historial de ventas."""
    producto.activo = False
    producto.save(update_fields=["activo", "actualizado"])
    return producto


def reactivar_producto(producto):
    producto.activo = True
    producto.save(update_fields=["activo", "actualizado"])
    return producto


# PR-03 Gestionar categorías
def crear_categoria(*, nombre, descripcion=""):
    nombre = nombre.strip()
    if Categoria.objects.filter(nombre__iexact=nombre).exists():
        raise ValidationError(f"Ya existe la categoría {nombre}.")
    return Categoria.objects.create(nombre=nombre, descripcion=descripcion)


def eliminar_categoria(categoria):
    if categoria.productos.exists():
        raise ValidationError("No se puede eliminar una categoría que tiene productos asociados.")
    categoria.delete()


# PR-04 Definir y actualizar precios
@transaction.atomic
def actualizar_precio(producto, nuevo_precio, usuario=None):
    _validar_precio(nuevo_precio)
    nuevo_precio = Decimal(nuevo_precio)
    if nuevo_precio == producto.precio_venta:
        return producto
    HistorialPrecio.objects.create(
        producto=producto,
        precio_anterior=producto.precio_venta,
        precio_nuevo=nuevo_precio,
        usuario=usuario,
    )
    producto.precio_venta = nuevo_precio
    producto.save(update_fields=["precio_venta", "actualizado"])
    return producto
