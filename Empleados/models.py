from django.db import models

class Empleado(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=45)
    carnet = models.CharField(max_length=16)
    rol = models.CharField(max_length=50)
    telefono = models.IntegerField()
    usuario = models.CharField(max_length=45, unique=True)
    clave = models.CharField(max_length=255)
    habilitado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'empleados'
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
