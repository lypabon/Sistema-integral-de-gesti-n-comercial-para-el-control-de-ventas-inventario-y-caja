from django.contrib import admin

from .models import Existencia, MovimientoInventario


@admin.register(Existencia)
class ExistenciaAdmin(admin.ModelAdmin):
    list_display = ("producto", "cantidad")
    readonly_fields = ("producto", "cantidad")


@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ("fecha", "producto", "tipo", "cantidad", "stock_resultante", "motivo", "usuario")
    list_filter = ("tipo",)
    readonly_fields = [f.name for f in MovimientoInventario._meta.fields]
