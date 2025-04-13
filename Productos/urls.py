from django.urls import path
from .views import *

urlpatterns = [
    path('productos/', lista_productos),
    path('productos/<int:id_producto>/', producto),
    path('productos/registrar/', registrar_producto),
    path('productos/actualizar/<int:id_producto>/', actualizar_producto),
    path('productos/eliminar/<int:id_producto>/', eliminar_producto),
]