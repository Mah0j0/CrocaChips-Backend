from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from django.db.models.functions import TruncDate
from Productos.models import LoteProduccion


@api_view(['GET'])
def produccion_mensual(request):
    data = LoteProduccion.objects.annotate(fecha=TruncDate('fecha_elaboracion')) \
        .values('fecha').annotate(total=Sum('cantidad'))
    return Response(data)

@api_view(['GET'])
def produccion_por_producto(request):
    data = LoteProduccion.objects.values('producto_id', 'producto__nombre') \
        .annotate(total=Sum('cantidad'))
    return Response(data)
