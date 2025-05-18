from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from Ventas.models import Venta
from Productos.models import Producto

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def alertas_realtime(request):
    # Alerta: Ventas pendientes por confirmar (estado=False)
    ventas_pendientes = Venta.objects.filter(estado=False).count()
    alerta_ventas = {
        "tipo": "ventas_pendientes",
        "mensaje": f"Hay {ventas_pendientes} venta(s) pendiente(s) por confirmar",
        "cantidad": ventas_pendientes
    }

    # Alerta: Productos sin stock
    productos_sin_stock = Producto.objects.filter(stock=0)
    alerta_stock = {
        "tipo": "productos_sin_stock",
        "mensaje": f"Hay {productos_sin_stock.count()} producto(s) sin stock",
        "productos": [p.nombre for p in productos_sin_stock]
    }

    # Alerta: Productos con stock bajo (menos de 10)
    productos_stock_bajo = Producto.objects.filter(stock__gt=0, stock__lt=10)
    alerta_bajo_stock = {
        "tipo": "productos_stock_bajo",
        "mensaje": f"Hay {productos_stock_bajo.count()} producto(s) con stock bajo",
        "productos": [f"{p.nombre} ({p.stock})" for p in productos_stock_bajo]
    }

    return Response({
        "alertas": [alerta_ventas, alerta_stock, alerta_bajo_stock]
    })
