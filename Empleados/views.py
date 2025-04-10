from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Empleado
from .serializers import EmpleadoSerializer
import bcrypt


@api_view(['GET'])
def lista_empleados(request):
    empleados = Empleado.objects.all()  # Obtiene todos los empleados
    serializer = EmpleadoSerializer(empleados, many=True)  # Serializa los empleados
    return Response(serializer.data)  # Devuelve los empleados serializados como respuesta JSON

@api_view(['GET'])
def empleado(request, id):
    try:
        empleado = Empleado.objects.get(id_empleado=id)  # Obtiene el empleado por ID
    except Empleado.DoesNotExist:
        return Response({'error': 'Empleado no encontrado'}, status=404)
    serializer = EmpleadoSerializer(empleado)
    return Response(serializer.data)

@api_view(['POST'])
def login_empleado(request):
    usuario = request.data.get('usuario')
    clave = request.data.get('clave')

    if not usuario or not clave:
        return Response({'error': 'Usuario y clave son requeridos'}, status=400)

    try:
        empleado = Empleado.objects.get(usuario=usuario)
    except Empleado.DoesNotExist:
        return Response({'error': 'Credenciales inválidas'}, status=401)

    clave_valida = bcrypt.checkpw(clave.encode('utf-8'), empleado.clave.encode('utf-8'))

    if not clave_valida:
        return Response({'error': 'Credenciales inválidas'}, status=401)

    # Si llega aquí, el login fue exitoso
    return Response({
        'id_empleado': empleado.id_empleado,
        'nombre': empleado.nombre,
        'apellido': empleado.apellido,
        'rol': empleado.rol,
        'usuario': empleado.usuario
    })