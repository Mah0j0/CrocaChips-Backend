from django.urls import path
from .views import *



urlpatterns = [
    path('dashboard/', InformacionGeneral),
    path('dashboard/ventas_mensuales/', ventas_mensuales),
    path('dashboard/ventas_semanales/', ventas_semanales),
    path('dashboard/ventas_vendedor/', ventas_vendedor),
    path('dashboard/ventas_productos/', ventas_productos),
]
