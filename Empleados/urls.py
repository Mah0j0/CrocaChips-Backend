from django.urls import path
from .views import *

urlpatterns = [
    path('empleados/', lista_empleados),
]
