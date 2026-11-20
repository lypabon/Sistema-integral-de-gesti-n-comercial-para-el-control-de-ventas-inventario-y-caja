from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from apps.productos.models import Categoria, Producto
from apps.usuarios.models import Rol, Usuario

from . import servicios
from .models import MovimientoInventario


class InventarioTest(TestCase):
    def setUp(self):
        cat = Categoria.objects.create(nombre="Papelería")
        self.p = Producto.objects.create(codigo="P1", nombre="Cuaderno", categoria=cat, precio_venta=Decimal("3000"), stock_minimo=5)
        self.bodega = Usuario.objects.create_user("bod", password="x", rol=Rol.BODEGA)

    def test_in01_entrada_suma_stock_y_deja_movimiento(self):
        servicios.registrar_entrada(self.p, 20, motivo="Compra", usuario=self.bodega)
        self.assertEqual(servicios.stock_de(self.p), 20)
        mov = MovimientoInventario.objects.get()
        self.assertEqual((mov.cantidad, mov.stock_resultante), (20, 20))

    def test_in01_no_acepta_cantidad_cero(self):
        with self.assertRaises(ValidationError):
            servicios.registrar_entrada(self.p, 0, motivo="Compra")

    def test_in02_salida_resta_stock(self):
        servicios.registrar_entrada(self.p, 10, motivo="Compra")
        servicios.registrar_salida(self.p, 4, motivo="Venta")
        self.assertEqual(servicios.stock_de(self.p), 6)

    def test_in02_no_deja_stock_negativo(self):
        servicios.registrar_entrada(self.p, 3, motivo="Compra")
        with self.assertRaises(servicios.StockInsuficiente):
            servicios.registrar_salida(self.p, 4, motivo="Venta")
        self.assertEqual(servicios.stock_de(self.p), 3)

    def test_in03_ajuste_registra_la_diferencia(self):
        servicios.registrar_entrada(self.p, 10, motivo="Compra")
        mov = servicios.ajustar_inventario(self.p, 8, motivo="Conteo mensual: 2 unidades dañadas")
        self.assertEqual(mov.cantidad, -2)
        self.assertEqual(servicios.stock_de(self.p), 8)

    def test_in03_ajuste_exige_motivo(self):
        with self.assertRaises(ValidationError):
            servicios.ajustar_inventario(self.p, 8, motivo="  ")

    def test_in04_alerta_cuando_stock_llega_al_minimo(self):
        servicios.registrar_entrada(self.p, 5, motivo="Compra")
        self.assertIn(self.p, servicios.productos_bajo_stock())
        servicios.registrar_entrada(self.p, 1, motivo="Compra")
        self.assertNotIn(self.p, servicios.productos_bajo_stock())

    def test_in04_producto_inactivo_no_genera_alerta(self):
        self.p.activo = False
        self.p.save()
        self.assertNotIn(self.p, servicios.productos_bajo_stock())

    def test_vendedor_no_puede_ajustar_inventario(self):
        vendedor = Usuario.objects.create_user("vend", password="x", rol=Rol.VENDEDOR)
        self.client.force_login(vendedor)
        self.assertEqual(self.client.get(reverse("inventario:ajuste")).status_code, 403)
