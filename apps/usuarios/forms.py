from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Usuario


class UsuarioCrearForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ("username", "first_name", "last_name", "email", "rol")


class UsuarioEditarForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ("first_name", "last_name", "email", "rol", "is_active")
        labels = {"is_active": "Activo"}
