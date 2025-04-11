from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Empleado
from .serializers import EmpleadoSerializer
import bcrypt

# Vista para obtener la lista de empleados, protegida por autenticación
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Requiere autenticación para acceder a esta vista
def lista_empleados(request):
    empleados = Empleado.objects.all()  # Obtiene todos los empleados
    serializer = EmpleadoSerializer(empleados, many=True)  # Serializa los empleados
    return Response(serializer.data)  # Devuelve los empleados serializados como respuesta JSON

# Vista para obtener un empleado específico por ID, protegida por autenticación
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Requiere autenticación para acceder a esta vista
def empleado(request, id):
    try:
        empleado = Empleado.objects.get(id=id)  # Cambié de 'id_empleado' a 'id'
    except Empleado.DoesNotExist:
        return Response({'error': 'Empleado no encontrado'}, status=404)
    serializer = EmpleadoSerializer(empleado)
    return Response(serializer.data)


# Vista para registrar un nuevo empleado
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def registrar_empleado(request):
    data = request.data

    # Validar campos requeridos
    campos = ['nombre', 'apellido', 'carnet', 'rol', 'telefono']
    for campo in campos:
        if campo not in data:
            return Response({'error': f'El campo {campo} es requerido'}, status=400)
    
    nombre = data['nombre'].strip()
    apellido = data['apellido'].strip()
    carnet = data['carnet'].strip()

    # Generar usuario: primera letra del nombre + apellido + dos primeros del carnet
    usuario_generado = f"{nombre[0].upper()}{apellido}{carnet[:2]}"

    # Verificar si el usuario ya existe
    if Empleado.objects.filter(usuario=usuario_generado).exists():
        return Response({'error': 'El usuario generado ya está registrado'}, status=409)

    # Generar clave: primera letra del nombre + primera del apellido + últimos 4 del carnet
    clave_generada = f"{nombre[0].upper()}{apellido[0].upper()}{carnet[-4:]}"
    clave_encriptada = bcrypt.hashpw(clave_generada.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    empleado = Empleado.objects.create(
        nombre=nombre,
        apellido=apellido,
        carnet=carnet,
        rol=data['rol'],
        telefono=data['telefono'],
        usuario=usuario_generado,
        clave=clave_encriptada,
        habilitado=data.get('habilitado', True)
    )

    serializer = EmpleadoSerializer(empleado)

    return Response({
        'empleado': serializer.data,
        'usuario_generado': usuario_generado,
        'clave_generada': clave_generada
    }, status=201)

# Vista de login para empleados (no requiere autenticación, se puede acceder sin token)
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


    refresh['id'] = empleado.id 

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'empleado': {
            'id': empleado.id,  # Usamos id_empleado en la respuesta
            'nombre': empleado.nombre,
            'apellido': empleado.apellido,
            'rol': empleado.rol,
            'usuario': empleado.usuario
        }
    })
