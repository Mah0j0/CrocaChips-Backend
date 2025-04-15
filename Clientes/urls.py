from django.urls import path
from .views import *

urlpatterns = [
    path('clientes/', lista_clientes),
    path('clientes/<int:id_cliente>/', cliente),
    path('clientes/registrar/', registrar_cliente),
    path('clientes/actualizar/<int:id_cliente>/', actualizar_cliente),
    path('clientes/eliminar/<int:id_cliente>/', eliminar_cliente),
]