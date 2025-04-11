from django.urls import path
from .views import *

urlpatterns = [
    path('empleados/', lista_empleados),
    path('empleados/<int:id>/', empleado),
    path('empleados/registrar/', registrar_empleado),
    path('login/', login_empleado),
]
