from django.urls import path
from .views import *

urlpatterns = [
    path('prediccion-ventas/', lista_prediccion_ventas,),
]
