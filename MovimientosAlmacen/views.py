from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import date
from django.db import connection
from .models import MovimientoAlmacen
from Productos.models import Producto
from Empleados.models import Empleado
from .serializers import MovimientoAlmacenSerializer

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
    with connection.cursor() as cursor:
        cursor.execute("DROP TRIGGER IF EXISTS after_update_stock")

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
        with connection.cursor() as cursor:
            cursor.execute("""
            CREATE TRIGGER after_update_stock
            AFTER UPDATE ON productos
            FOR EACH ROW
            BEGIN
                DECLARE cantidad_nueva INT;

                -- Verificar si el stock ha aumentado
                IF NEW.stock > OLD.stock THEN
                    SET cantidad_nueva = NEW.stock - OLD.stock;
                    
                    -- Si ya existe un lote para este producto hoy, actualiza
                    IF EXISTS (
                        SELECT 1 FROM lotes_produccion
                        WHERE id_producto = NEW.id_producto AND fecha_elaboracion = CURDATE()
                    ) THEN
                        UPDATE lotes_produccion
                        SET cantidad = cantidad + cantidad_nueva
                        WHERE id_producto = NEW.id_producto AND fecha_elaboracion = CURDATE();
                    ELSE
                        INSERT INTO lotes_produccion (id_producto, cantidad, fecha_elaboracion)
                        VALUES (NEW.id_producto, cantidad_nueva, CURDATE());
                    END IF;
                END IF;
            END;
            """)

        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)
