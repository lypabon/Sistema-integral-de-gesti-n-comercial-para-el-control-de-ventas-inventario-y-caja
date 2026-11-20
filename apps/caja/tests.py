from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.usuarios.models import Rol, Usuario

from . import servicios
from .models import Caja, MedioPago, MovimientoCaja

D = Decimal


class CajaTest(TestCase):
    def setUp(self):
        self.vend = Usuario.objects.create_user("vend", password="x", rol=Rol.VENDEDOR)
        self.caja = servicios.abrir_caja(self.vend, D("100000"))

    def test_cj01_no_permite_dos_cajas_abiertas(self):
        with self.assertRaises(ValidationError):
            servicios.abrir_caja(self.vend, D("50000"))

    def test_cj03_movimiento_exige_motivo(self):
        with self.assertRaises(ValidationError):
            servicios.registrar_movimiento(self.caja, MovimientoCaja.Tipo.EGRESO, D("1000"), motivo="")

    def test_cj03_egreso_no_supera_el_efectivo(self):
        with self.assertRaises(ValidationError):
            servicios.registrar_movimiento(self.caja, MovimientoCaja.Tipo.EGRESO, D("100001"), motivo="Pago proveedor")

    def test_cj02_formula_de_cuadre(self):
        servicios.registrar_cobro_de_venta(self.caja, D("30000"), MedioPago.EFECTIVO, referencia="V-1")
        servicios.registrar_cobro_de_venta(self.caja, D("50000"), MedioPago.TARJETA, referencia="V-2")
        servicios.registrar_movimiento(self.caja, MovimientoCaja.Tipo.INGRESO, D("5000"), motivo="Sencillo")
        servicios.registrar_movimiento(self.caja, MovimientoCaja.Tipo.EGRESO, D("12000"), motivo="Aseo")
        # 100.000 + 30.000 + 5.000 − 12.000 = 123.000 (la tarjeta no es efectivo)
        self.assertEqual(servicios.efectivo_esperado(self.caja), D("123000"))

    def test_cj02_cierre_cuadrado(self):
        caja = servicios.cerrar_caja(self.caja, D("100000"))
        self.assertEqual(caja.estado, Caja.Estado.CERRADA)
        self.assertEqual(caja.diferencia, D("0"))

    def test_cj02_descuadre_exige_observacion(self):
        with self.assertRaises(ValidationError):
            servicios.cerrar_caja(self.caja, D("98000"))
        caja = servicios.cerrar_caja(self.caja, D("98000"), observacion="Faltante por cambio mal entregado")
        self.assertEqual(caja.diferencia, D("-2000"))

    def test_cj02_caja_cerrada_no_recibe_movimientos(self):
        servicios.cerrar_caja(self.caja, D("100000"))
        with self.assertRaises(ValidationError):
            servicios.registrar_movimiento(self.caja, MovimientoCaja.Tipo.INGRESO, D("1000"), motivo="X")
