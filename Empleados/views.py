from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Empleado
from .serializers import EmpleadoSerializer


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
