from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from apps.usuarios.models import Rol, Usuario

from . import servicios
from .models import Categoria, HistorialPrecio, Producto


class ServiciosProductosTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Papelería")
        self.admin = Usuario.objects.create_user("admin1", password="x", rol=Rol.ADMINISTRADOR)

    def _producto(self, codigo="P001", precio="2500"):
        return servicios.registrar_producto(
            codigo=codigo, nombre="Cuaderno", categoria=self.categoria, precio_venta=Decimal(precio), usuario=self.admin
        )

    def test_pr01_registra_producto_y_su_precio_inicial(self):
        p = self._producto()
        self.assertEqual(p.codigo, "P001")
        self.assertEqual(p.historial_precios.count(), 1)

    def test_pr01_no_permite_codigo_duplicado(self):
        self._producto("p001")
        with self.assertRaises(ValidationError):
            self._producto("P001")

    def test_pr01_no_permite_precio_cero(self):
        with self.assertRaises(ValidationError):
            self._producto(precio="0")

    def test_pr02_inactivar_conserva_el_producto(self):
        p = self._producto()
        servicios.inactivar_producto(p)
        p.refresh_from_db()
        self.assertFalse(p.activo)
        self.assertTrue(Producto.objects.filter(pk=p.pk).exists())

    def test_pr03_no_elimina_categoria_con_productos(self):
        self._producto()
        with self.assertRaises(ValidationError):
            servicios.eliminar_categoria(self.categoria)

    def test_pr03_no_permite_categoria_duplicada(self):
        with self.assertRaises(ValidationError):
            servicios.crear_categoria(nombre="papelería")

    def test_pr04_cambio_de_precio_queda_en_historial(self):
        p = self._producto(precio="2500")
        servicios.actualizar_precio(p, Decimal("2800"), usuario=self.admin)
        ultimo = HistorialPrecio.objects.filter(producto=p).first()
        self.assertEqual(ultimo.precio_anterior, Decimal("2500"))
        self.assertEqual(ultimo.precio_nuevo, Decimal("2800"))
        self.assertEqual(p.historial_precios.count(), 2)

    def test_pr04_mismo_precio_no_genera_registro(self):
        p = self._producto(precio="2500")
        servicios.actualizar_precio(p, Decimal("2500"))
        self.assertEqual(p.historial_precios.count(), 1)


class PermisosProductosTest(TestCase):
    def setUp(self):
        self.vendedor = Usuario.objects.create_user("vend", password="x", rol=Rol.VENDEDOR)
        self.bodega = Usuario.objects.create_user("bod", password="x", rol=Rol.BODEGA)

    def test_vendedor_puede_consultar_pero_no_crear(self):
        self.client.force_login(self.vendedor)
        self.assertEqual(self.client.get(reverse("productos:lista")).status_code, 200)
        self.assertEqual(self.client.get(reverse("productos:crear")).status_code, 403)

    def test_bodega_puede_crear_pero_no_cambiar_precios(self):
        self.client.force_login(self.bodega)
        cat = Categoria.objects.create(nombre="Ferretería")
        r = self.client.post(
            reverse("productos:crear"),
            {"codigo": "F01", "nombre": "Martillo", "categoria": cat.pk, "precio_venta": "18000", "stock_minimo": 2},
        )
        self.assertEqual(r.status_code, 302)
        p = Producto.objects.get(codigo="F01")
        self.assertEqual(self.client.get(reverse("productos:precio", args=[p.pk])).status_code, 403)

    def test_sin_sesion_redirige_a_ingresar(self):
        r = self.client.get(reverse("productos:lista"))
        self.assertEqual(r.status_code, 302)
        self.assertIn(reverse("login"), r.url)
