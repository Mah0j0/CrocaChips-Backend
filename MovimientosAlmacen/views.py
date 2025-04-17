from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import date
from django.db import connection
from .models import MovimientoAlmacen
from Productos.models import Producto
from Empleados.models import Empleado
from .serializers import MovimientoAlmacenSerializer
from .utils import eliminar_trigger_stock, crear_trigger_stock

# lista de movimientos del tipo 'Despacho' - (GET)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lista_despachos(request):
    despachos = MovimientoAlmacen.objects.filter(tipo_movimiento='Despacho')
    serializer = MovimientoAlmacenSerializer(despachos, many=True)
    return Response(serializer.data)

# lista de movimientos del tipo 'Recepcion' - (GET)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lista_recepciones(request):
    recepciones = MovimientoAlmacen.objects.filter(tipo_movimiento='Recepcion')
    serializer = MovimientoAlmacenSerializer(recepciones, many=True)
    return Response(serializer.data)

# obtener un movimiento por ID - (GET)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movimiento(request, id_movimiento):
    try:
        movimiento = MovimientoAlmacen.objects.get(id_movimiento=id_movimiento)
    except MovimientoAlmacen.DoesNotExist:
        return Response({'error': 'Movimiento no encontrado'}, status=404)
    
    serializer = MovimientoAlmacenSerializer(movimiento)
    return Response(serializer.data)

# registrar_despacho - (POST)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def registrar_despacho(request):
    data = request.data
    data['tipo_movimiento'] = 'Despacho'
    data['cantidad_volatil'] = data.get('cantidad')  # Asignar cantidad_volatil igual a cantidad

    serializer = MovimientoAlmacenSerializer(data=data)

    try:
        producto = Producto.objects.get(id_producto=data.get('producto'))
        empleado = Empleado.objects.get(id=data.get('vendedor'))
    except Empleado.DoesNotExist:
        return Response({'error': 'Empleado no encontrado'}, status=404)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=404)
    

    cantidad = int(data.get('cantidad'))

    if cantidad > producto.stock:
        return Response({'error': 'No hay suficiente stock para realizar el despacho'}, status=400)

    if serializer.is_valid():
        serializer.save()
        producto.stock -= cantidad
        producto.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)

# registrar_recepcion - (POST)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def registrar_recepcion(request):
    data = request.data
    data['tipo_movimiento'] = 'Recepcion'
    data['cantidad_volatil'] = 0  # Siempre 0 para devoluciones

    serializer = MovimientoAlmacenSerializer(data=data)

    try:
        producto = Producto.objects.get(id_producto=data.get('producto'))
        empleado = Empleado.objects.get(id=data.get('vendedor'))
    except Empleado.DoesNotExist:
        return Response({'error': 'Empleado no encontrado'}, status=404)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=404)

    cantidad = int(data.get('cantidad'))

    # Desactivar temporalmente el trigger para evitar que se actualice lotes_produccion
    eliminar_trigger_stock()

    if serializer.is_valid():
        serializer.save()
        producto.stock += cantidad
        producto.save()

        # Obtener fecha actual (hoy)
        fecha_actual = date.today()

        # Buscar y actualizar los despachos del mismo día para ese producto y vendedor
        MovimientoAlmacen.objects.filter(
            producto=producto,
            vendedor=empleado,
            tipo_movimiento='Despacho',
            fecha=fecha_actual
        ).update(cantidad_volatil=0)

        # Volver a crear el trigger después de realizar las modificaciones
        crear_trigger_stock()

        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)

# actualizar_despacho - (PUT)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def actualizar_despacho(request):
    id_despacho = request.data.get('id_movimiento')

    try:
        movimiento = MovimientoAlmacen.objects.get(id_movimiento=id_despacho)
        producto = Producto.objects.get(id_producto=request.data.get('producto'))
        empleado = Empleado.objects.get(id=request.data.get('vendedor'))
    except MovimientoAlmacen.DoesNotExist:
        return Response({'error': 'Movimiento de despacho no encontrado'}, status=404)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=404)
    except Empleado.DoesNotExist:
        return Response({'error': 'Empleado no encontrado'}, status=404)

    cantidad = int(request.data.get('cantidad'))

    if cantidad > producto.stock:
        return Response({'error': 'No hay suficiente stock para realizar el despacho'}, status=400)

    diferencia_cantidad = cantidad - movimiento.cantidad

    # Desactivar temporalmente el trigger
    eliminar_trigger_stock()

    # Actualizar los campos del movimiento
    movimiento.cantidad = cantidad
    movimiento.cantidad_volatil = cantidad
    movimiento.fecha = request.data.get('fecha', movimiento.fecha)
    movimiento.save()

    # Actualizar stock
    if diferencia_cantidad < 0:
        producto.stock += abs(diferencia_cantidad)
    else:
        producto.stock -= abs(diferencia_cantidad)
    producto.save()

    # Reactivar el trigger
    crear_trigger_stock()

    return Response(MovimientoAlmacenSerializer(movimiento).data, status=200)


# actualizar_recepcion - (PUT)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def actualizar_recepcion(request):
    id_recepcion = request.data.get('id_movimiento')

    try:
        movimiento = MovimientoAlmacen.objects.get(id_movimiento=id_recepcion)
        producto = Producto.objects.get(id_producto=request.data.get('producto'))
        empleado = Empleado.objects.get(id=request.data.get('vendedor'))
    except MovimientoAlmacen.DoesNotExist:
        return Response({'error': 'Movimiento de recepción no encontrado'}, status=404)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=404)
    except Empleado.DoesNotExist:
        return Response({'error': 'Empleado no encontrado'}, status=404)

    cantidad = int(request.data.get('cantidad'))
    diferencia_cantidad = cantidad - movimiento.cantidad

    # Desactivar temporalmente el trigger
    eliminar_trigger_stock()

    # Actualización de los campos del movimiento
    movimiento.cantidad = cantidad
    movimiento.cantidad_volatil = 0  # Siempre 0 para recepciones
    movimiento.fecha = request.data.get('fecha', movimiento.fecha)
    movimiento.save()

    # Actualizar stock del producto (aumentar)
    if diferencia_cantidad > 0:
        producto.stock += diferencia_cantidad
    elif diferencia_cantidad < 0:
        producto.stock -= abs(diferencia_cantidad)
    producto.save()

    # Reactivar el trigger
    crear_trigger_stock()

    return Response(MovimientoAlmacenSerializer(movimiento).data, status=200)

# eliminar_despacho - (DELETE)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_despacho(request):
    id_despacho = request.data.get('id_movimiento')

    try:
        movimiento = MovimientoAlmacen.objects.get(id_movimiento=id_despacho)
        producto = Producto.objects.get(id_producto=movimiento.producto.id_producto)
    except MovimientoAlmacen.DoesNotExist:
        return Response({'error': 'Movimiento de despacho no encontrado'}, status=404)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=404)

    # Desactivar temporalmente el trigger
    eliminar_trigger_stock()

    # Actualizar stock del producto (aumentar)
    producto.stock += movimiento.cantidad
    producto.save()

    # Eliminar el movimiento
    movimiento.delete()

    # Reactivar el trigger
    crear_trigger_stock()

    return Response({'mensaje': 'Movimiento de despacho eliminado correctamente'}, status=200)

# eliminar_recepcion - (DELETE)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_recepcion(request):
    id_recepcion = request.data.get('id_movimiento')

    try:
        movimiento = MovimientoAlmacen.objects.get(id_movimiento=id_recepcion)
        producto = Producto.objects.get(id_producto=movimiento.producto.id_producto)
    except MovimientoAlmacen.DoesNotExist:
        return Response({'error': 'Movimiento de recepción no encontrado'}, status=404)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=404)

    # Desactivar temporalmente el trigger
    eliminar_trigger_stock()

    # Actualizar stock del producto (disminuir)
    producto.stock -= movimiento.cantidad
    producto.save()

    # Eliminar el movimiento
    movimiento.delete()

    # Reactivar el trigger
    crear_trigger_stock()

    return Response({'mensaje': 'Movimiento de recepción eliminado correctamente'}, status=200)