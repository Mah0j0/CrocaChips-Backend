from django.urls import path
from .views import *



urlpatterns = [
    path('dashboard/', InformacionGeneral),
    path('dashboard/ventas_mensuales/', ventas_mensuales),
    path('dashboard/ventas_semanales/', ventas_semanales),
]
