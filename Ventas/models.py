from django.db import models
from Empleados.models import Empleado
from Clientes.models import Cliente

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