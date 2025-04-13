from django.urls import path
from .views import *

urlpatterns = [
    path('productos/', lista_productos),
    path('productos/<int:id>/', producto),
    path('productos/registrar/', registrar_producto),
    path('productos/actualizar/<int:id>/', actualizar_producto),
    path('productos/eliminar/<int:id>/', eliminar_producto),
]