from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Cliente
from .serializers import ClienteSerializer

# lista_clientes - (GET)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lista_clientes(request):
    clientes = Cliente.objects.all() # Listar clientes
    serializer = ClienteSerializer(clientes, many=True) # Serializar
    return Response(serializer.data) # Retornar datos en formato JSON

# cliente - (GET)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cliente(request, id_cliente):
    try:
        cliente = Cliente.objects.get(id_cliente=id_cliente) # Buscar cliente por ID
    except Cliente.DoesNotExist:
        return Response({'error': 'Cliente no encontrado'}, status=404)
    serializer = ClienteSerializer(cliente) # Serializar y retornar el cliente
    return Response(serializer.data)

# registrar_cliente - (POST)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def registrar_cliente(request):
    data = request.data
    
    # Validar campos requeridos
    campos = ['nombre', 'direccion', 'telefono']
    for campo in campos:
        if campo not in data:
            return Response({'error': f'El campo {campo} es requerido'}, status=400)
    
    serializer = ClienteSerializer(data=data)
    if serializer.is_valid(): # Validar datos
        serializer.save() # Crar cliente
        return Response(serializer.data, status=201) # Created
    return Response(serializer.errors, status=400) # Bad Request

# actualizar_cliente - (PUT)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def actualizar_cliente(request):

    data = request.data
    id_cliente = data.get('id_cliente')
    if not id_cliente:
        return Response({'error': 'El campo id_cliente es requerido'}, status=400)
    try:
        cliente = Cliente.objects.get(id_cliente=id_cliente) # Buscar cliente por ID
    except Cliente.DoesNotExist:
        return Response({'error': 'Cliente no encontrado'}, status=404)
    
    serializer = ClienteSerializer(cliente, data=request.data, partial=True) # Actualización parcial
    if serializer.is_valid(): # Validar datos
        serializer.save() # Guardar cambios
        return Response(
            {'mensaje': 'Cliente actualizado correctamente', 'data': serializer.data},
            status=200
        ) # Modified
    return Response(serializer.errors, status=400) # Bad Request

# eliminar_cliente - (DELETE)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_cliente(request):
    data = request.data
    id_cliente = data.get('id_cliente')
    if not id_cliente:
        return Response({'error': 'El campo id_cliente es requerido'}, status=400)
    try:
        cliente = Cliente.objects.get(id_cliente=id_cliente)
    except Cliente.DoesNotExist:
        return Response({'error': 'Cliente no encontrado'}, status=404)
    
    cliente.habilitado = False
    cliente.save()
    serializer = ClienteSerializer(cliente)

    return Response({'mensaje': 'Cliente eliminado correctamente', 'Cliente': serializer.data}, status=200)
