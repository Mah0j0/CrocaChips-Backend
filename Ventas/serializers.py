from rest_framework import serializers
from .models import Venta, DetalleVenta

class VentaSerializer(serializers.ModelSerializer):
    vendedor_nombre = serializers.SerializerMethodField()
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)

    class Meta:
        model = Venta
        fields = [
            'id_venta',
            'vendedor',
            'cliente',
            'vendedor_nombre',
            'cliente_nombre',
            'estado',
            'fecha',
            'precio_total',
        ]

    def get_vendedor_nombre(self, obj):
        return f"{obj.vendedor.nombre} {obj.vendedor.apellido}"

class DetalleVentaSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)

    class Meta:
        model = DetalleVenta
        fields = [
            'id_detalle',
            'id_venta',
            'producto',
            'producto_nombre',
            'cantidad',
            'precio_unitario',
            'subtotal',
        ]
        