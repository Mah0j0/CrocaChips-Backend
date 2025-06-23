from django.urls import path
from .views import *
from .dashviews import ventas, inventario, produccion, clientes

urlpatterns = [
    path('dashboard/', InformacionGeneral),
    path('dashboard/ventas_mensuales/', ventas_mensuales),
    path('dashboard/ventas_semanales/', ventas_semanales),
    path('dashboard/ventas_vendedor/', ventas_vendedor),
    path('dashboard/ventas_productos/', ventas_productos),

    path('dashboard/ventas/mensual/', ventas.total_ventas_mensual),
    path('dashboard/ventas/top-productos/', ventas.productos_mas_vendidos),
    path('dashboard/ventas/vendedor/', ventas.ventas_por_vendedor),
    path('dashboard/ventas/ticket-promedio/', ventas.ticket_promedio),
    path('dashboard/ventas/tendencia/', ventas.tendencia_ventas),

    path('dashboard/inventario/stock/', inventario.stock_actual),
    path('dashboard/inventario/bajo-stock/', inventario.productos_bajo_stock),
    path('dashboard/inventario/movimientos/', inventario.movimientos_por_producto),

    path('dashboard/produccion/mensual/', produccion.produccion_mensual),
    path('dashboard/produccion/por-producto/', produccion.produccion_por_producto),

    path('dashboard/clientes/frecuentes/', clientes.clientes_frecuentes),
    path('dashboard/clientes/nuevos-mensual/', clientes.nuevos_clientes_por_mes),
]
