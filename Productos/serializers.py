from rest_framework import serializers
from .models import Producto, LoteProduccion

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class LoteProduccionSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    class Meta:
        model = LoteProduccion
        fields = ['id_lote', 'producto', 'producto_nombre', 'cantidad', 'fecha_elaboracion']