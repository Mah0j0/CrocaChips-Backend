from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from Clientes.models import Cliente
from Ventas.models import Venta


@api_view(['GET'])
def clientes_frecuentes(request):
    data = Venta.objects.values('cliente_id', 'cliente__nombre') \
        .annotate(compras=Count('id_venta')).order_by('-compras')[:10]
    return Response(data)

@api_view(['GET'])
def nuevos_clientes_por_mes(request):
    data = Cliente.objects.annotate(mes=TruncMonth('created_at')) \
        .values('mes').annotate(total=Count('id_cliente'))
    return Response(data)
