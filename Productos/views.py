from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Producto, LoteProduccion
from .serializers import ProductoSerializer, LoteProduccionSerializer

# lista_productos - (GET)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lista_productos(request):
    # Parámetros de filtrado
    habilitado = request.query_params.get('habilitado')
    orden_precio = request.query_params.get('precio')
    orden_alfabetico = request.query_params.get('alfabetico')
    
    # Listado de productos
    productos = Producto.objects.all()

    # Habilitado-No habilitado
    if habilitado is not None:
        habilitado_bool = habilitado.lower() == 'true' # String -> Booleano
        productos = productos.filter(habilitado=habilitado_bool)

    # Ordenar por precio
    if orden_precio:
        if orden_precio.lower() == 'mayor':
            productos = productos.order_by('-precio_unitario')  # Descendente
        elif orden_precio.lower() == 'menor':
            productos = productos.order_by('precio_unitario')  # Ascendente

    # Ordenar alfabeticamente
    if orden_alfabetico:
        if orden_alfabetico.lower() == 'asc':
            productos = productos.order_by('nombre') # A-Z
        elif orden_alfabetico.lower() == 'desc':
            productos = productos.order_by('-nombre') # Z-A

    serializer = ProductoSerializer(productos, many=True) # Serializar
    return Response(serializer.data) # Retornar datos en formato JSON


# producto - (GET)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def producto(request, id_producto):
    try:
        producto = Producto.objects.get(id_producto=id_producto) # Buscar producto por ID
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=404)
    serializer = ProductoSerializer(producto) # Serializar y retornar el producto
    return Response(serializer.data)


# registrar_producto - (POST)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def registrar_producto(request):
    data = request.data

    # Validar campos requeridos
    campos = ['nombre', 'descripcion', 'tiempo_vida', 'precio_unitario', 'stock']
    for campo in campos:
        if campo not in data:
            return Response({'error': f'El campo {campo} es requerido'}, status=400)
        
    if data['stock'] <= 0:
        return Response({'error': 'El stock debe ser mayor a 0'}, status=400)
    
    if data['precio_unitario'] <= 0:
        return Response({'error' : 'El precio unitario debe ser mayor a 0'}, status=400)

    serializer = ProductoSerializer(data=data)
    if serializer.is_valid(): # Validar datos
        serializer.save() # Crar producto
        return Response(serializer.data, status=201) # Created
    return Response(serializer.errors, status=400) # Bad Request


# actualizar_producto - (PUT)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def actualizar_producto(request):
    data = request.data
    id_producto = data.get('id_producto')
    if not id_producto:
        return Response({'error': 'El campo id_producto es requerido'}, status=400)
    try:
        producto = Producto.objects.get(id_producto=id_producto) # Buscar producto por ID
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=404)
    # Actualización parcial
    serializer = ProductoSerializer(producto, data=request.data, partial=True) # Actualización parcial
    if serializer.is_valid(): # Validar datos
        serializer.save() # Guardar cambios
        return Response(
            {'mensaje': 'Producto actualizado correctamente', 'Producto': serializer.data}, 
            status=200
        )
        
    return Response(serializer.errors, status=400) # Bad Request


# eliminar_producto - (DELETE)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_producto(request):
    data = request.data
    id_producto = data.get('id_producto')
    if not id_producto:
        return Response({'error': 'El campo id_producto es requerido'}, status=400)
    try:
        producto = Producto.objects.get(id_producto=id_producto)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=404)

    producto.habilitado = False
    producto.save()   
    serializer = ProductoSerializer(producto)
    return Response({'mensaje': 'Producto eliminado correctamente', 'Producto': serializer.data}, status=200)

# Obtener los lotes de producción

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lista_lotes(request):
    lotes = LoteProduccion.objects.all()
    serializer = LoteProduccionSerializer(lotes, many=True)
    return Response(serializer.data)

# aumentar_stock - (PATCH)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def aumentar_stock(request):
    data = request.data
    id_producto = data.get('id_producto')
    cantidad = data.get('cantidad')

    if not id_producto or not cantidad:
        return Response({'error': 'Los campos id_producto y cantidad son requeridos'}, status=400)

    try:
        producto = Producto.objects.get(id_producto=id_producto)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=404)
    serializer = ProductoSerializer(producto, data=request.data, partial=True)
    if serializer.is_valid():
        producto.stock += cantidad
        producto.save()
        serializer = ProductoSerializer(producto)
        return Response(
            {'mensaje': 'Stock aumentado correctamente', 'Producto': serializer.data}, 
            status=200
        )
    return Response(serializer.errors, status=400)


# disminuir_stock - (PATCH)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def disminuir_stock(request):
    data = request.data
    id_producto = data.get('id_producto')
    cantidad = data.get('cantidad')

    if not id_producto or not cantidad:
        return Response({'error': 'Los campos id_producto y cantidad son requeridos'}, status=400)

    try:
        producto = Producto.objects.get(id_producto=id_producto)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=404)

    if producto.stock < cantidad:
        return Response({'error': 'No hay suficiente stock'}, status=400)

    serializer = ProductoSerializer(producto, data=request.data, partial=True)
    if serializer.is_valid():
        producto.stock -= cantidad
        producto.save()
        serializer = ProductoSerializer(producto)
        return Response(
            {'mensaje': 'Stock aumentado correctamente', 'Producto': serializer.data}, 
            status=200
        )
    return Response(serializer.errors, status=400)