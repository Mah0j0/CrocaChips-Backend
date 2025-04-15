from django.urls import path
from .views import *

urlpatterns = [
    path('productos/', lista_productos),
    path('productos/<int:id_producto>/', producto),
    path('productos/registrar/', registrar_producto),
    path('productos/actualizar/', actualizar_producto),
    path('productos/eliminar/', eliminar_producto),
]