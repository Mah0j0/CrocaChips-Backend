from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (TokenRefreshView)
urlpatterns = [
    path('empleados/', lista_empleados),
    path('empleados/<int:id>/', empleado),
    path('empleados/registrar/', registrar_empleado),
    path('empleados/actualizar/<int:id>/', actualizar_empleado),
    path('empleados/deshabilitar/<int:id>/', deshabilitar_empleado),
    path('mi-perfil/', mi_perfil, name='mi-perfil'),
    # Rutas de autenticación
    path('login/', login_empleado),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # ¡La ruta de refresco!

]
