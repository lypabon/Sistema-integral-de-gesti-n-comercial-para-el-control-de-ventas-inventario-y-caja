"""Capa de presentación del módulo Caja."""
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render

from apps.usuarios.permisos import permiso_requerido, puede

from . import servicios
from .forms import AperturaForm, CierreForm, MovimientoForm
from .models import Caja


@permiso_requerido("caja.operar")
def mi_caja(request):
    caja = servicios.caja_abierta_de(request.user)
    if caja is None:
        form = AperturaForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            try:
                servicios.abrir_caja(request.user, form.cleaned_data["fondo_inicial"])
                messages.success(request, "Caja abierta.")
                return redirect("caja:mi_caja")
            except ValidationError as e:
                form.add_error(None, e)
        return render(request, "caja/abrir.html", {"form": form})
    contexto = {
        "caja": caja,
        "resumen": servicios.resumen(caja),
        "esperado": servicios.efectivo_esperado(caja),
        "form_mov": MovimientoForm(),
        "form_cierre": CierreForm(),
    }
    return render(request, "caja/mi_caja.html", contexto)


@permiso_requerido("caja.operar")
def movimiento(request):
    caja = servicios.caja_abierta_de(request.user)
    form = MovimientoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        d = form.cleaned_data
        try:
            servicios.registrar_movimiento(caja, d["tipo"], d["monto"], motivo=d["motivo"], usuario=request.user)
            messages.success(request, "Movimiento registrado.")
        except ValidationError as e:
            messages.error(request, e.messages[0])
    return redirect("caja:mi_caja")


@permiso_requerido("caja.operar")
def cerrar(request):
    caja = servicios.caja_abierta_de(request.user)
    form = CierreForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            caja = servicios.cerrar_caja(caja, form.cleaned_data["efectivo_contado"], observacion=form.cleaned_data["observacion"], usuario=request.user)
            messages.success(request, "Caja cerrada.")
            return redirect("caja:detalle", pk=caja.pk)
        except ValidationError as e:
            messages.error(request, e.messages[0])
    return redirect("caja:mi_caja")


@permiso_requerido("caja.operar")
def detalle(request, pk):
    caja = get_object_or_404(Caja, pk=pk)
    if caja.responsable != request.user and not puede(request.user, "reportes.consultar"):
        return redirect("caja:mi_caja")
    return render(request, "caja/detalle.html", {"caja": caja, "resumen": servicios.resumen(caja)})


@permiso_requerido("reportes.consultar")
def historial(request):
    return render(request, "caja/historial.html", {"cajas": Caja.objects.select_related("responsable")[:100]})
