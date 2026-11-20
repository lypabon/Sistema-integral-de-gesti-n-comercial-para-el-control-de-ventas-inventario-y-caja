from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.caja import servicios as caja_srv
from apps.caja.models import MedioPago
from apps.inventario import servicios as inv_srv
from apps.productos.models import Categoria, Producto
from apps.usuarios.models import Rol, Usuario

from . import servicios
from .models import Venta

D = Decimal


@override_settings(VENTAS_IVA="0.19", VENTAS_DESCUENTO_MAX="10")
class VentasTest(TestCase):
    def setUp(self):
        cat = Categoria.objects.create(nombre="Papelería")
        self.cuaderno = Producto.objects.create(codigo="C1", nombre="Cuaderno", categoria=cat, precio_venta=D("3000"))
        self.lapiz = Producto.objects.create(codigo="L1", nombre="Lápiz", categoria=cat, precio_venta=D("1000"))
        inv_srv.registrar_entrada(self.cuaderno, 10, motivo="Compra")
        inv_srv.registrar_entrada(self.lapiz, 10, motivo="Compra")
        self.vend = Usuario.objects.create_user("vend", password="x", rol=Rol.VENDEDOR)
        self.caja = caja_srv.abrir_caja(self.vend, D("50000"))

    def _vender(self, lineas=None, **kw):
        kw.setdefault("medio_pago", MedioPago.EFECTIVO)
        kw.setdefault("monto_recibido", D("100000"))
        return servicios.registrar_venta(self.vend, lineas or [(self.cuaderno, 2), (self.lapiz, 3)], **kw)

    def test_ve02_calculo_con_descuento_e_iva(self):
        t = servicios.calcular_totales([(self.cuaderno, 2), (self.lapiz, 3)], descuento_pct=10)
        # subtotal 9.000; descuento 900; base 8.100; IVA 1.539; total 9.639
        self.assertEqual((t["subtotal"], t["descuento"], t["impuesto"], t["total"]), (D("9000"), D("900"), D("1539"), D("9639")))

    def test_ve02_descuento_mayor_al_maximo_se_rechaza(self):
        with self.assertRaises(ValidationError):
            servicios.calcular_totales([(self.cuaderno, 1)], descuento_pct=15)

    def test_ve01_venta_descuenta_inventario(self):
        self._vender()
        self.assertEqual(inv_srv.stock_de(self.cuaderno), 8)
        self.assertEqual(inv_srv.stock_de(self.lapiz), 7)

    def test_ve01_lineas_repetidas_se_agrupan(self):
        venta = self._vender([(self.lapiz, 1), (self.lapiz, 2)])
        self.assertEqual(venta.detalles.get().cantidad, 3)

    def test_ve01_sin_stock_no_se_registra_nada(self):
        with self.assertRaises(ValidationError):
            self._vender([(self.cuaderno, 2), (self.lapiz, 11)])
        self.assertEqual(Venta.objects.count(), 0)
        self.assertEqual(inv_srv.stock_de(self.cuaderno), 10)  # la salida del cuaderno se deshizo
        self.assertEqual(self.caja.movimientos.count(), 0)

    def test_ve01_sin_caja_abierta_no_se_vende(self):
        otro = Usuario.objects.create_user("otro", password="x", rol=Rol.VENDEDOR)
        with self.assertRaises(ValidationError):
            servicios.registrar_venta(otro, [(self.lapiz, 1)], medio_pago=MedioPago.TARJETA)

    def test_ve01_producto_inactivo_no_se_vende(self):
        self.lapiz.activo = False
        self.lapiz.save()
        with self.assertRaises(ValidationError):
            self._vender([(self.lapiz, 1)])

    def test_ve03_numeracion_consecutiva(self):
        a, b = self._vender(), self._vender([(self.lapiz, 1)])
        self.assertEqual((a.numero, b.numero), ("V-000001", "V-000002"))

    def test_ve04_efectivo_insuficiente_se_rechaza(self):
        with self.assertRaises(ValidationError):
            self._vender(monto_recibido=D("1000"))

    def test_ve04_cambio_y_cobro_en_caja(self):
        venta = self._vender(monto_recibido=D("20000"))
        self.assertEqual(venta.total, D("10710"))  # 9.000 + 19 % IVA
        self.assertEqual(venta.cambio, D("9290"))
        self.assertEqual(caja_srv.efectivo_esperado(self.caja), D("60710"))

    def test_ve04_pago_con_tarjeta_no_suma_efectivo(self):
        self._vender(medio_pago=MedioPago.TARJETA, monto_recibido=None)
        self.assertEqual(caja_srv.efectivo_esperado(self.caja), D("50000"))
        self.assertEqual(caja_srv.resumen(self.caja)["ventas_tarjeta"], D("10710"))

    def test_bodega_no_puede_vender(self):
        bodega = Usuario.objects.create_user("bod", password="x", rol=Rol.BODEGA)
        self.client.force_login(bodega)
        self.assertEqual(self.client.get(reverse("ventas:nueva")).status_code, 403)

    def test_flujo_web_de_venta(self):
        self.client.force_login(self.vend)
        datos = {
            "l-TOTAL_FORMS": "5", "l-INITIAL_FORMS": "0", "l-MIN_NUM_FORMS": "0", "l-MAX_NUM_FORMS": "1000",
            "l-0-producto": self.cuaderno.pk, "l-0-cantidad": "1",
            "descuento_pct": "0", "medio_pago": "EFECTIVO", "monto_recibido": "5000",
        }
        r = self.client.post(reverse("ventas:nueva"), datos)
        venta = Venta.objects.get()
        self.assertRedirects(r, reverse("ventas:comprobante", args=[venta.pk]))
        self.assertContains(self.client.get(r.url), "V-000001")
