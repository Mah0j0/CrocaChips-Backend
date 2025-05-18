from django.urls import path
from .views import alertas_realtime

urlpatterns = [
    path('alertas/', alertas_realtime),
]