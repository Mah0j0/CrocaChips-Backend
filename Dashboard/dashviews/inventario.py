from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum

from MovimientosAlmacen.models import MovimientoAlmacen
from Productos.models import Producto


@api_view(['GET'])
def stock_actual(request):
    data = Producto.objects.values('nombre', 'stock').order_by('stock')
    return Response(data)

@api_view(['GET'])
def productos_bajo_stock(request):
    data = Producto.objects.filter(stock__lt=50).values('nombre', 'stock')
    return Response(data)

@api_view(['GET'])
def movimientos_por_producto(request):
    data = MovimientoAlmacen.objects.values('producto_id', 'producto__nombre', 'tipo_movimiento') \
        .annotate(total=Sum('cantidad'))
    return Response(data)
