from django.db import models
from Empleados.models import Empleado
from Productos.models import Producto

class MovimientoAlmacen(models.Model):
    id_movimiento = models.AutoField(primary_key=True, db_column='id_movimiento')
    vendedor = models.ForeignKey(Empleado, on_delete=models.CASCADE, db_column='id_vendedor', related_name='movimientos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='id_producto', related_name='movimientos')
    tipo_movimiento = models.CharField(max_length=50) # 'Despacho' o 'Recepcion'
    cantidad = models.IntegerField()
    cantidad_volatil = models.IntegerField()
    fecha = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'movimientos_almacen'

    def __str__(self):
        return f'Movimiento {self.id_movimiento} - {self.tipo_movimiento}'