from rest_framework import serializers
from .models import MovimientoAlmacen

class MovimientoAlmacenSerializer(serializers.ModelSerializer):
    vendedor_nombre = serializers.SerializerMethodField() 
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)

    class Meta:
        model = MovimientoAlmacen
        fields = [
            'id_movimiento',
            'vendedor',
            'producto',
            'vendedor_nombre',
            'producto_nombre',
            'tipo_movimiento',
            'cantidad',
            'cantidad_volatil',
            'fecha',
        ]

    def get_vendedor_nombre(self, obj):
        return f"{obj.vendedor.nombre} {obj.vendedor.apellido}"
