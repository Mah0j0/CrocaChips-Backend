
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Venta, DetalleVenta
from Productos.models import Producto
from MovimientosAlmacen.models import MovimientoAlmacen
from Empleados.models import Empleado
from Clientes.models import Cliente
from .serializers import VentaSerializer, DetalleVentaSerializer
from datetime import date
from django.db import transaction

# lista de ventas y sus detalles - (GET)
@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def lista_ventas(request):
    # Usamos select_related para optimizar el acceso a las relaciones de vendedor y cliente
    ventas = Venta.objects.select_related('vendedor', 'cliente').all()  # Optimización de relaciones
    data = []

    for venta in ventas:
        venta_serializer = VentaSerializer(venta)

        data.append({
            'venta': venta_serializer.data
        })

    return Response(data)



# lista de una venta y sus detalles - (GET)
@api_view(['POST'])  # Cambio a POST
@permission_classes([IsAuthenticated])  
def detalles(request):
    # Verificamos si el 'id_venta' está en el cuerpo de la solicitud
    id_venta = request.data.get('id_venta', None)
    
    if not id_venta:
        return Response({'error': 'El campo id_venta es requerido.'}, status=400)
    
    try:
        # Recuperamos la venta usando el id_venta
        venta = Venta.objects.get(id_venta=id_venta)
    except Venta.DoesNotExist:
        return Response({'error': 'Venta no encontrada'}, status=404)
    
    # Recuperamos los detalles de la venta
    detalles = DetalleVenta.objects.filter(id_venta=venta.id_venta)
    
    # Serializamos solo los detalles de la venta
    detalle_serializer = DetalleVentaSerializer(detalles, many=True)

    # Devolvemos la respuesta con los detalles
    return Response({
        'detalles': detalle_serializer.data
    }, status=200)
    

# registrar venta - (POST)
@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def registrar_venta(request):
    data = request.data
    print(data)  # Agregar esto para ver qué datos está recibiendo el backend
    detalles = data.get('detalles', [])  # Los detalles pueden ser vacíos en este paso
    id_cliente = data.get('cliente')

    if not id_cliente:
        return Response({'error': 'Cliente no especificado'}, status=400)

    # Obtener el empleado autenticado
    try:
        vendedor = Empleado.objects.get(usuario=request.user)
    except Empleado.DoesNotExist:
        return Response({'error': 'Vendedor no encontrado'}, status=404)

    try:
        cliente = Cliente.objects.get(id_cliente=id_cliente)
    except Cliente.DoesNotExist:
        return Response({'error': 'Cliente no encontrado'}, status=404)

    # Crear la venta con precio_total = 0 (por ahora)
    venta = Venta.objects.create(
        vendedor=vendedor,
        cliente=cliente,
        estado=0,
        fecha=date.today(),
        precio_total=0  # El precio total se actualizará cuando se agreguen los detalles
    )

    # Respuesta sin detalles
    venta_serializer = VentaSerializer(venta)
    return Response({
        'venta': venta_serializer.data
    }, status=201)


# # agregar detalles a la venta (POST)
@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def agregar_detalles_venta(request):
    data = request.data
    id_venta = data.get('venta')
    detalles = data.get('detalles', [])

    if not detalles or not id_venta:
        return Response({'error': 'Datos incompletos'}, status=400)

    # Obtener la venta
    try:
        venta = Venta.objects.get(id_venta=id_venta)
    except Venta.DoesNotExist:
        return Response({'error': 'Venta no encontrada'}, status=404)

    total = 0

    for detalle in detalles:
        id_producto = detalle.get('producto')
        cantidad = int(detalle.get('cantidad'))

        try:
            producto = Producto.objects.get(id_producto=id_producto)
        except Producto.DoesNotExist:
            return Response({'error': f'Producto {id_producto} no encontrado'}, status=404)

        precio_unitario = producto.precio_unitario
        subtotal = cantidad * precio_unitario

        # Verificar y descontar de los movimientos tipo 'Despacho' del vendedor
        movimientos = MovimientoAlmacen.objects.filter(
            tipo_movimiento='Despacho',
            vendedor=venta.vendedor,
            producto=producto,
            cantidad_volatil__gt=0
        ).order_by('fecha')

        cantidad_restante = cantidad

        for mov in movimientos:
            if cantidad_restante == 0:
                break
            if mov.cantidad_volatil >= cantidad_restante:
                mov.cantidad_volatil -= cantidad_restante
                mov.save()
                cantidad_restante = 0
            else:
                cantidad_restante -= mov.cantidad_volatil
                mov.cantidad_volatil = 0
                mov.save()

        if cantidad_restante > 0:
            return Response({'error': f'No hay suficiente cantidad disponible del producto {producto.nombre}'}, status=400)

        DetalleVenta.objects.create(
            id_venta=venta,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            subtotal=subtotal
        )

        total += subtotal

    # Actualizar precio_total
    venta.precio_total = total
    venta.save()

    venta_serializer = VentaSerializer(venta)
    detalles_serializer = DetalleVentaSerializer(DetalleVenta.objects.filter(id_venta=venta.id_venta), many=True)

    return Response({
        'venta': venta_serializer.data,
        'detalles': detalles_serializer.data
    }, status=201)
