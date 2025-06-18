from django.urls import path
from .views import *

urlpatterns = [
    path('prediccion-general/', lista_prediccion_general,),
    path('prediccion-productos/', lista_prediccion_producto,),
]
