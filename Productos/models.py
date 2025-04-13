from django.db import models

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True, db_column='id_producto')
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    tiempo_vida = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    habilitado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'productos'

    def __str__(self):
        return self.nombre
