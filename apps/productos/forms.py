from django import forms

from .models import Categoria


class ProductoForm(forms.Form):
    codigo = forms.CharField(max_length=30, label="Código")
    nombre = forms.CharField(max_length=120)
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), label="Categoría")
    precio_venta = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.01, label="Precio de venta")
    stock_minimo = forms.IntegerField(min_value=0, initial=0, label="Stock mínimo")


class ProductoEditarForm(forms.Form):
    nombre = forms.CharField(max_length=120)
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), label="Categoría")
    stock_minimo = forms.IntegerField(min_value=0, label="Stock mínimo")


class PrecioForm(forms.Form):
    precio_venta = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.01, label="Nuevo precio")


class CategoriaForm(forms.Form):
    nombre = forms.CharField(max_length=80)
    descripcion = forms.CharField(max_length=200, required=False, label="Descripción")
