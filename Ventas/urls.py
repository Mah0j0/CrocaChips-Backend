from django.urls import path
from .views import *

urlpatterns = [
    path('ventas/', lista_ventas),
    path('ventas/detalles/', detalles),
    path('ventas/registrar/', registrar_venta),
    path('ventas/confirmar/', confirmar_venta),
]