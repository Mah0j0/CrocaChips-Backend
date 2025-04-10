from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Empleado
from .serializers import EmpleadoSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
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

    # Verificar la clave usando bcrypt
    clave_valida = bcrypt.checkpw(clave.encode('utf-8'), empleado.clave.encode('utf-8'))

    if not clave_valida:
        return Response({'error': 'Credenciales inválidas'}, status=401)

    # Si la autenticación fue exitosa, generamos el token
    refresh = RefreshToken.for_user(empleado)

    # Añadimos 'id_empleado' manualmente al token
    refresh['id'] = empleado.id

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'empleado': {
            'id': empleado.id,
            'nombre': empleado.nombre,
            'apellido': empleado.apellido,
            'rol': empleado.rol,
            'usuario': empleado.usuario
        }
    })