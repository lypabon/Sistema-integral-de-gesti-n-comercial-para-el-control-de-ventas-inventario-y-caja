"""Capa de presentación del módulo Gestión de Inventario."""
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from apps.productos.models import Producto
from apps.usuarios.permisos import permiso_requerido

from . import servicios
from .forms import AjusteForm, EntradaForm
from .models import MovimientoInventario


@permiso_requerido("inventario.gestionar")
def existencias(request):
    productos = Producto.objects.filter(activo=True).select_related("categoria", "existencia").order_by("nombre")
    filas = [(p, servicios.stock_de(p)) for p in productos]
    alertas = servicios.productos_bajo_stock()
    return render(request, "inventario/existencias.html", {"filas": filas, "alertas": alertas})


@permiso_requerido("inventario.gestionar")
def entrada(request):
    form = EntradaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        d = form.cleaned_data
        try:
            servicios.registrar_entrada(d["producto"], d["cantidad"], motivo=d["motivo"], usuario=request.user, referencia=d["referencia"])
            messages.success(request, "Entrada registrada.")
            return redirect("inventario:existencias")
        except ValidationError as e:
            form.add_error(None, e)
    return render(request, "formulario.html", {"form": form, "titulo": "Registrar entrada de inventario"})


@permiso_requerido("inventario.gestionar")
def ajuste(request):
    form = AjusteForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        d = form.cleaned_data
        try:
            mov = servicios.ajustar_inventario(d["producto"], d["conteo_fisico"], motivo=d["motivo"], usuario=request.user)
            messages.success(request, "Ajuste registrado." if mov else "El conteo coincide con el sistema; no hubo ajuste.")
            return redirect("inventario:existencias")
        except ValidationError as e:
            form.add_error(None, e)
    return render(request, "formulario.html", {"form": form, "titulo": "Ajustar inventario"})


@permiso_requerido("inventario.gestionar")
def movimientos(request):
    movs = MovimientoInventario.objects.select_related("producto", "usuario")[:200]
    return render(request, "inventario/movimientos.html", {"movimientos": movs})
