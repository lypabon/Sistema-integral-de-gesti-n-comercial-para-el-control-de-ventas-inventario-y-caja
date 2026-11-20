"""Capa de presentación del módulo Gestión de Ventas."""
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render

from apps.caja import servicios as caja_srv
from apps.usuarios.permisos import permiso_requerido, puede

from . import servicios
from .forms import LineaFormSet, PagoForm
from .models import Venta


@permiso_requerido("ventas.registrar")
def nueva_venta(request):
    if caja_srv.caja_abierta_de(request.user) is None:
        messages.error(request, "Debe abrir la caja antes de vender.")
        return redirect("caja:mi_caja")
    lineas_fs = LineaFormSet(request.POST or None, prefix="l")
    pago = PagoForm(request.POST or None)
    if request.method == "POST" and lineas_fs.is_valid() and pago.is_valid():
        lineas = [(f.cleaned_data["producto"], f.cleaned_data["cantidad"]) for f in lineas_fs
                  if f.cleaned_data.get("producto") and f.cleaned_data.get("cantidad")]
        try:
            venta = servicios.registrar_venta(request.user, lineas, **pago.cleaned_data)
            messages.success(request, f"Venta {venta.numero} registrada.")
            return redirect("ventas:comprobante", pk=venta.pk)
        except ValidationError as e:
            pago.add_error(None, e)
    contexto = {"lineas": lineas_fs, "pago": pago, "iva": servicios.iva() * 100, "desc_max": servicios.descuento_maximo()}
    return render(request, "ventas/nueva.html", contexto)


@permiso_requerido("ventas.registrar")
def comprobante(request, pk):
    venta = get_object_or_404(Venta.objects.select_related("vendedor", "caja"), pk=pk)
    if venta.vendedor != request.user and not puede(request.user, "reportes.consultar"):
        return redirect("ventas:lista")
    return render(request, "ventas/comprobante.html", {"venta": venta, "detalles": venta.detalles.select_related("producto")})


@permiso_requerido("ventas.registrar")
def lista(request):
    ventas = Venta.objects.select_related("vendedor")
    if not puede(request.user, "reportes.consultar"):
        ventas = ventas.filter(vendedor=request.user)
    return render(request, "ventas/lista.html", {"ventas": ventas[:100]})
