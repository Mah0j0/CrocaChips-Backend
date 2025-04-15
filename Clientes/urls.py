from django.urls import path
from .views import *

urlpatterns = [
    path('clientes/', lista_clientes),
    path('clientes/<int:id_cliente>/', cliente),
    path('clientes/registrar/', registrar_cliente),
    path('clientes/actualizar/', actualizar_cliente),
    path('clientes/eliminar/', eliminar_cliente),
]