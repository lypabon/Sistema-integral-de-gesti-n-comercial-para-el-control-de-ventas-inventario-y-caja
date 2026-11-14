from django.test import TestCase
from django.urls import reverse

from .models import Rol, Usuario
from .permisos import puede


class UsuariosYRolesTest(TestCase):
    def setUp(self):
        self.admin = Usuario.objects.create_user("admin1", password="x", rol=Rol.ADMINISTRADOR)
        self.vendedor = Usuario.objects.create_user("vend", password="x", rol=Rol.VENDEDOR)

    def test_us01_administrador_crea_usuario_con_rol(self):
        self.client.force_login(self.admin)
        r = self.client.post(
            reverse("usuarios:crear"),
            {"username": "bodega1", "rol": Rol.BODEGA, "password1": "Clave-Segura-2026", "password2": "Clave-Segura-2026"},
        )
        self.assertEqual(r.status_code, 302)
        nuevo = Usuario.objects.get(username="bodega1")
        self.assertEqual(nuevo.rol, Rol.BODEGA)
        self.assertNotEqual(nuevo.password, "Clave-Segura-2026")  # contraseña guardada cifrada

    def test_us02_vendedor_no_gestiona_usuarios(self):
        self.client.force_login(self.vendedor)
        self.assertEqual(self.client.get(reverse("usuarios:lista")).status_code, 403)

    def test_us02_matriz_de_permisos(self):
        self.assertTrue(puede(self.vendedor, "ventas.registrar"))
        self.assertFalse(puede(self.vendedor, "reportes.consultar"))
        self.assertTrue(puede(self.admin, "reportes.consultar"))
