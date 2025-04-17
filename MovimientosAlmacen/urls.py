from django.urls import path
from .views import *

urlpatterns = [
    path('movimientos/despachos/', lista_despachos),
    path('movimientos/despachos/registrar/', registrar_despacho),

    path('movimientos/recepciones/', lista_recepciones),
    path('movimientos/recepciones/registrar/', registrar_recepcion),

    path('movimientos/<int:id_movimiento>/', movimiento),
]