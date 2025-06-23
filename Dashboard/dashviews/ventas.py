from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum, Count, Avg

from Ventas.models import Venta, DetalleVenta


@api_view(['GET'])
def total_ventas_mensual(request):
    data = Venta.objects.extra({'mes': "MONTH(fecha)"}).values('mes').annotate(total=Sum('precio_total'))
    return Response(data)

@api_view(['GET'])
def productos_mas_vendidos(request):
    data = DetalleVenta.objects.values('producto_id', 'producto__nombre') \
        .annotate(total_vendido=Sum('cantidad')) \
        .order_by('-total_vendido')[:10]
    return Response(data)

@api_view(['GET'])
def ventas_por_vendedor(request):
    data = Venta.objects.values('vendedor_id', 'vendedor__nombre') \
        .annotate(total=Sum('precio_total'))
    return Response(data)

@api_view(['GET'])
def ticket_promedio(request):
    promedio = Venta.objects.aggregate(promedio=Avg('precio_total'))
    return Response(promedio)
