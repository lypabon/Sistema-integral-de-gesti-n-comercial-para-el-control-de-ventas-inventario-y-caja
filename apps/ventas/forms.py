from django import forms

from apps.caja.models import MedioPago
from apps.productos.models import Producto


class LineaForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=Producto.objects.filter(activo=True), required=False)
    cantidad = forms.IntegerField(min_value=1, required=False)


LineaFormSet = forms.formset_factory(LineaForm, extra=5)


class PagoForm(forms.Form):
    descuento_pct = forms.DecimalField(max_digits=5, decimal_places=2, min_value=0, initial=0, label="Descuento (%)")
    medio_pago = forms.ChoiceField(choices=MedioPago.choices, label="Medio de pago")
    monto_recibido = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0, required=False, label="Efectivo recibido")
