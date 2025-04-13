from rest_framework import serializers
from .models import Empleado

class EmpleadoSerializer(serializers.ModelSerializer):
        class Meta:
                model = Empleado
                fields = ('id', 'nombre', 'apellido', 'rol', 'usuario', 'telefono', 'habilitado', 'carnet')
