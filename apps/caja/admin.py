from django.contrib import admin

from .models import Caja, MovimientoCaja


class MovimientoInline(admin.TabularInline):
    model = MovimientoCaja
    extra = 0
    readonly_fields = ("tipo", "medio_pago", "monto", "motivo", "referencia", "fecha", "usuario")
    can_delete = False


@admin.register(Caja)
class CajaAdmin(admin.ModelAdmin):
    list_display = ("id", "responsable", "estado", "abierta_en", "cerrada_en", "diferencia")
    list_filter = ("estado",)
    inlines = [MovimientoInline]
