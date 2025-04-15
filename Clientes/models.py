from django.db import models

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True, db_column='id_cliente')
    nombre = models.CharField(max_length=30)
    direccion = models.CharField(max_length=255)
    telefono = models.IntegerField()
    habilitado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    class Meta:
        db_table = 'clientes'
    
    def __str__(self):
        return self.nombre
