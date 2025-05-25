from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum
from django.db import models
from Empleados.models import Empleado
from Productos.models import Producto
from Clientes.models import Cliente
from Ventas.models import Venta 
from django.utils import timezone
from django.db.models.functions import ExtractMonth, ExtractDay
from .utils import mapear_meses, mapear_semana
from datetime import timedelta

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def InformacionGeneral(request):
    cantidad_empleados = Empleado.objects.count()
    cantidad_clientes = Cliente.objects.count()
    
    suma_productos = Producto.objects.filter(habilitado=True).aggregate(total=Sum('stock'))['total'] or 0
    suma_ventas = Venta.objects.filter(estado=True).aggregate(total=Sum('precio_total'))['total'] or 0

    return Response({
        'cantidad_empleados': cantidad_empleados,
        'cantidad_productos': suma_productos,
        'cantidad_clientes': cantidad_clientes,
        'total_ventas': suma_ventas,
    })


