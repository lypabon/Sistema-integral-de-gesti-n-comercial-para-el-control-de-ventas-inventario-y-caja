from django.contrib import admin

from .models import Categoria, HistorialPrecio, Producto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    search_fields = ("nombre",)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "categoria", "precio_venta", "stock_minimo", "activo")
    list_filter = ("activo", "categoria")
    search_fields = ("codigo", "nombre")


@admin.register(HistorialPrecio)
class HistorialPrecioAdmin(admin.ModelAdmin):
    list_display = ("producto", "precio_anterior", "precio_nuevo", "fecha", "usuario")
    readonly_fields = ("producto", "precio_anterior", "precio_nuevo", "fecha", "usuario")
