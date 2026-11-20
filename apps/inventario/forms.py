from django import forms

from apps.productos.models import Producto


class EntradaForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=Producto.objects.filter(activo=True))
    cantidad = forms.IntegerField(min_value=1)
    motivo = forms.CharField(max_length=200, initial="Compra de mercancía")
    referencia = forms.CharField(max_length=50, required=False, help_text="Número de factura o de compra (opcional).")


class AjusteForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=Producto.objects.filter(activo=True))
    conteo_fisico = forms.IntegerField(min_value=0, label="Conteo físico")
    motivo = forms.CharField(max_length=200, help_text="Obligatorio: explique la diferencia.")
