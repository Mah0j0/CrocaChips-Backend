from django.urls import path
from .views import *

urlpatterns = [
    path('ventas/', lista_ventas),
    path('ventas/detalles/', detalles),
    path('ventas/registrar/', registrar_venta),
    path('ventas/agregar-detalle/', agregar_detalles_venta),
]