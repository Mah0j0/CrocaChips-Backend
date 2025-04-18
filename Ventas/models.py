from django.db import models
from Empleados.models import Empleado
from Clientes.models import Cliente
from Productos.models import Producto

class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True, db_column='id_venta')
    vendedor = models.ForeignKey(Empleado, on_delete=models.CASCADE, db_column='id_vendedor', related_name='ventas')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='id_cliente', related_name='ventas')
    estado = models.BooleanField(default=True)  # True = Activo, False = Inactivo
    fecha = models.DateField(auto_now_add=True)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'ventas'

    def __str__(self):
        return f'Venta {self.id_venta} - {self.vendedor} - {self.cliente} - {self.fecha}'
        
class DetalleVenta(models.Model):
    id_detalle = models.AutoField(primary_key=True, db_column='id_detalle')
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE, db_column='id_venta', related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='id_producto', related_name='detalles')
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'detalle_venta'
    
    def __str__(self):
        return f'Detalle Venta {self.id_detalle} - Venta {self.id_venta} - Producto {self.producto} - Cantidad {self.cantidad}'