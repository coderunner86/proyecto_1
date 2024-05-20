from django.db import models

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200, blank=True)
    tipo = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=100)
    longitud = models.FloatField(default=0, null=True)
    latitud = models.FloatField(default=0, null=True)
    estado_geo = models.BooleanField(default=False)
    cargo = models.CharField(max_length=50, null=True, blank=True)
