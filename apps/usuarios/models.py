"""Capa de persistencia del módulo Usuarios y Roles (US-01, US-02)."""
from django.contrib.auth.models import AbstractUser
from django.db import models


class Rol(models.TextChoices):
    ADMINISTRADOR = "ADMIN", "Administrador"
    VENDEDOR = "VENDEDOR", "Vendedor"
    BODEGA = "BODEGA", "Encargado de bodega"


class Usuario(AbstractUser):
    """Usuario del sistema con un único rol que define lo que puede hacer."""

    rol = models.CharField(max_length=10, choices=Rol.choices, default=Rol.VENDEDOR)

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"

    def tiene_rol(self, *roles):
        """True si el usuario es superusuario o tiene alguno de los roles dados."""
        return self.is_superuser or self.rol in roles

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_rol_display()})"
