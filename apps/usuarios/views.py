"""Capa de presentación del módulo Usuarios y Roles."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import UsuarioCrearForm, UsuarioEditarForm
from .models import Usuario
from .permisos import permiso_requerido


@login_required
def inicio(request):
    return render(request, "inicio.html")


@permiso_requerido("usuarios.gestionar")
def lista_usuarios(request):
    usuarios = Usuario.objects.order_by("username")
    return render(request, "usuarios/lista.html", {"usuarios": usuarios})


@permiso_requerido("usuarios.gestionar")
def crear_usuario(request):
    form = UsuarioCrearForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Usuario creado.")
        return redirect("usuarios:lista")
    return render(request, "formulario.html", {"form": form, "titulo": "Nuevo usuario"})


@permiso_requerido("usuarios.gestionar")
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    form = UsuarioEditarForm(request.POST or None, instance=usuario)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Usuario actualizado.")
        return redirect("usuarios:lista")
    return render(request, "formulario.html", {"form": form, "titulo": f"Editar {usuario.username}"})
