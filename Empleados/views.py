from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Empleado
from .serializers import EmpleadoSerializer
import bcrypt


# Obtener todos los empleados (autenticado)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lista_empleados(request):
    empleados = Empleado.objects.all()
    serializer = EmpleadoSerializer(empleados, many=True)
    return Response(serializer.data)

# Obtener perfil del empleado autenticado
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mi_perfil(request):
    try:
        empleado = Empleado.objects.get(usuario=request.user)
    except Empleado.DoesNotExist:
        return Response({'error': 'Empleado no encontrado'}, status=404)

    serializer = EmpleadoSerializer(empleado)
    return Response(serializer.data)

# Obtener un empleado por ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def empleado(request, id):
    try:
        empleado = Empleado.objects.get(id=id)
    except Empleado.DoesNotExist:
        return Response({'error': 'Empleado no encontrado'}, status=404)

    serializer = EmpleadoSerializer(empleado)
    return Response(serializer.data)

# Registrar nuevo empleado
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def registrar_empleado(request):
    data = request.data

    campos_requeridos = ['nombre', 'apellido', 'carnet', 'rol', 'telefono']
    for campo in campos_requeridos:
        if not data.get(campo):
            return Response({'error': f'El campo {campo} es requerido'}, status=400)

    nombre = data['nombre'].strip()
    apellido = data['apellido'].strip()
    carnet = data['carnet'].strip()

    usuario_generado = f"{nombre[0].upper()}{apellido.split()[0]}{carnet[:2]}"

    if Empleado.objects.filter(usuario=usuario_generado).exists():
        return Response({'error': 'El usuario generado ya está registrado'}, status=409)
    
    if Empleado.objects.filter(carnet=carnet).exists():
        return Response({'error': 'El carnet ya está registrado'}, status=409)
    
    if Empleado.objects.filter(telefono=data['telefono']).exists():
        return Response({'error': 'El teléfono ya está registrado'}, status=409)

    if not len(str(data['carnet'])) >= 5 or not len(str(data['carnet'])) <= 10:
        return Response({'error': 'El carnet debe tener entre 5 y 10 dígitos'}, status=400)
    
    if not str(data['telefono']).isdigit() or str(data['telefono'])[0] not in ['6', '7'] or len(str(data['telefono'])) != 8:
        return Response({'error': 'El teléfono debe ser válido'}, status=400)

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

# Actualizar empleado
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def actualizar_empleado(request):
    data = request.data
    empleado_id = data.get('id')

    if not empleado_id:
        return Response({'error': 'ID del empleado es requerido'}, status=400)

    try:
        empleado = Empleado.objects.get(id=empleado_id)
    except Empleado.DoesNotExist:
        return Response({'error': 'Empleado no encontrado'}, status=404)

    empleado.nombre = data.get('nombre', empleado.nombre)
    empleado.apellido = data.get('apellido', empleado.apellido)
    empleado.rol = data.get('rol', empleado.rol)
    empleado.telefono = data.get('telefono', empleado.telefono)
    empleado.save()

    serializer = EmpleadoSerializer(empleado)
    return Response({'mensaje': 'Empleado actualizado correctamente', 'empleado': serializer.data}, status=200)


# Deshabilitar empleado (borrado lógico)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deshabilitar_empleado(request):
    data = request.data
    empleado_id = data.get('id')

    if not empleado_id:
        return Response({'error': 'ID del empleado es requerido'}, status=400)
    
    try:
        empleado = Empleado.objects.get(id=empleado_id)
    except Empleado.DoesNotExist:
        return Response({'error': 'Empleado no encontrado'}, status=404)

    empleado.habilitado = False
    empleado.save()
    serializer = EmpleadoSerializer(empleado)
    return Response({'mensaje': 'Empleado deshabilitado correctamente', 'empleado': serializer.data}, status=200)

# Login de empleado (sin autenticación previa)
@api_view(['POST'])
def login_empleado(request):
    usuario = request.data.get('usuario', '').strip()
    clave = request.data.get('clave', '').strip()

    # Validar campos requeridos
    if not usuario or not clave:
        return Response({'error': 'Usuario y clave son requeridos'}, status=400)

    try:
        empleado = Empleado.objects.get(usuario=usuario)
    except Empleado.DoesNotExist:
        return Response({'error': 'Credenciales inválidas'}, status=401)

    # Verificar la contraseña
    if not bcrypt.checkpw(clave.encode('utf-8'), empleado.clave.encode('utf-8')):
        return Response({'error': 'Credenciales inválidas'}, status=401)

    # Verificar si el empleado está habilitado
    if not empleado.habilitado:
        return Response({'error': 'Empleado deshabilitado. Contacte al administrador.'}, status=403)

    # Generar tokens JWT
    refresh = RefreshToken.for_user(empleado)
    refresh['id'] = empleado.id  # Puedes añadir más campos si quieres (como rol, nombre, etc.)

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=200)