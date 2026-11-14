"""Capa de presentación del módulo Gestión de Productos."""
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.usuarios.permisos import permiso_requerido

from . import servicios
from .forms import CategoriaForm, PrecioForm, ProductoEditarForm, ProductoForm
from .models import Categoria, Producto


@permiso_requerido("productos.consultar")
def lista_productos(request):
    q = request.GET.get("q", "").strip()
    productos = Producto.objects.select_related("categoria")
    if q:
        productos = productos.filter(nombre__icontains=q) | productos.filter(codigo__icontains=q)
    return render(request, "productos/lista.html", {"productos": productos, "q": q})


@permiso_requerido("productos.gestionar")
def crear_producto(request):
    form = ProductoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            servicios.registrar_producto(usuario=request.user, **form.cleaned_data)
            messages.success(request, "Producto registrado.")
            return redirect("productos:lista")
        except ValidationError as e:
            form.add_error(None, e)
    return render(request, "formulario.html", {"form": form, "titulo": "Nuevo producto"})


@permiso_requerido("productos.gestionar")
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    inicial = {"nombre": producto.nombre, "categoria": producto.categoria, "stock_minimo": producto.stock_minimo}
    form = ProductoEditarForm(request.POST or None, initial=inicial)
    if request.method == "POST" and form.is_valid():
        servicios.editar_producto(producto, **form.cleaned_data)
        messages.success(request, "Producto actualizado.")
        return redirect("productos:lista")
    return render(request, "formulario.html", {"form": form, "titulo": f"Editar {producto}"})


@require_POST
@permiso_requerido("productos.gestionar")
def cambiar_estado(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if producto.activo:
        servicios.inactivar_producto(producto)
        messages.info(request, f"{producto} inactivado. Su historial se conserva.")
    else:
        servicios.reactivar_producto(producto)
        messages.success(request, f"{producto} reactivado.")
    return redirect("productos:lista")


@permiso_requerido("productos.precios")
def cambiar_precio(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    form = PrecioForm(request.POST or None, initial={"precio_venta": producto.precio_venta})
    if request.method == "POST" and form.is_valid():
        servicios.actualizar_precio(producto, form.cleaned_data["precio_venta"], usuario=request.user)
        messages.success(request, "Precio actualizado.")
        return redirect("productos:lista")
    historial = producto.historial_precios.select_related("usuario")
    return render(request, "productos/precio.html", {"form": form, "producto": producto, "historial": historial})


@permiso_requerido("productos.gestionar")
def categorias(request):
    form = CategoriaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            servicios.crear_categoria(**form.cleaned_data)
            messages.success(request, "Categoría creada.")
            return redirect("productos:categorias")
        except ValidationError as e:
            form.add_error(None, e)
    return render(request, "productos/categorias.html", {"form": form, "categorias": Categoria.objects.all()})


@require_POST
@permiso_requerido("productos.gestionar")
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    try:
        servicios.eliminar_categoria(categoria)
        messages.success(request, "Categoría eliminada.")
    except ValidationError as e:
        messages.error(request, e.messages[0])
    return redirect("productos:categorias")
