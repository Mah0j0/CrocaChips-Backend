from django.db.models.functions import ExtractMonth
from django.db.models import Sum
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import timedelta, date
import calendar

from Empleados.models import Empleado
from Productos.models import Producto
from Clientes.models import Cliente
from Ventas.models import Venta 
from .utils import *


@api_view(['GET'])
def ventas_mensuales(request):
    año_actual = timezone.now().year

    ventas = Venta.objects.filter(
        estado=True,
        fecha__year=año_actual
    ).annotate(
        mes=ExtractMonth('fecha')
    ).values('mes')
    ventas = ventas.annotate(total=Sum('precio_total')).order_by('mes')

    # Inicializar categorías y datos con todos los meses
    categorias = [MESES[i] for i in range(1, 13)]
    datos = [0] * 12

    # Rellenar con los valores reales de ventas
    for v in ventas:
        datos[v['mes'] - 1] = v['total']

    return Response({
        "categorias": categorias,
        "series": [
            {
                "nombre": "Ventas Mensuales",
                "datos": datos
            }
        ]
    })


@api_view(['GET'])
def ventas_semanales(request):
    hoy = timezone.now().date()
    año_actual, mes_actual = hoy.year, hoy.month

    # Obtener primer y último día del mes actual
    _, dias_en_mes = calendar.monthrange(año_actual, mes_actual)
    inicio_mes = date(año_actual, mes_actual, 1)
    fin_mes = date(año_actual, mes_actual, dias_en_mes)

    # Generar rango de semanas (lista de tuplas: (número, inicio, fin))
    semanas = []
    actual = inicio_mes
    numero_semana = 1
    while actual <= fin_mes:
        inicio_semana = actual
        fin_semana = min(actual + timedelta(days=6), fin_mes)
        semanas.append((numero_semana, inicio_semana, fin_semana))
        actual = fin_semana + timedelta(days=1)
        numero_semana += 1

    # Consultar totales por semana y construir listas para categorías y datos
    categorias = [
        obtener_nombre_semana(num, ini, fin) for num, ini, fin in semanas
    ]
    datos = [
        Venta.objects.filter(estado=True, fecha__range=[ini, fin])
            .aggregate(total=Sum('precio_total'))['total'] or 0
        for _, ini, fin in semanas
    ]

    return Response({
        "categorias": categorias,
        "series": [
            {
                "nombre": "Ventas Semanales",
                "datos": datos
            }
        ]
    })



@api_view(['GET'])
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
