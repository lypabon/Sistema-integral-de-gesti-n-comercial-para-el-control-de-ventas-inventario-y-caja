from django.contrib import admin

from .models import DetalleVenta, Venta


class DetalleInline(admin.TabularInline):
    model = DetalleVenta
    extra = 0
    readonly_fields = ("producto", "cantidad", "precio_unitario", "subtotal")
    can_delete = False


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ("numero", "fecha", "vendedor", "medio_pago", "total")
    list_filter = ("medio_pago",)
    search_fields = ("numero",)
    inlines = [DetalleInline]
