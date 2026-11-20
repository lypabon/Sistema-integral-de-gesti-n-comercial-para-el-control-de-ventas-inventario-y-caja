from django import forms

from .models import MovimientoCaja


class AperturaForm(forms.Form):
    fondo_inicial = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0, label="Fondo inicial en efectivo")


class MovimientoForm(forms.Form):
    tipo = forms.ChoiceField(choices=[(MovimientoCaja.Tipo.INGRESO, "Ingreso"), (MovimientoCaja.Tipo.EGRESO, "Egreso")])
    monto = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.01)
    motivo = forms.CharField(max_length=200)


class CierreForm(forms.Form):
    efectivo_contado = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0, label="Efectivo contado")
    observacion = forms.CharField(max_length=300, required=False, label="Observación (obligatoria si hay descuadre)")
