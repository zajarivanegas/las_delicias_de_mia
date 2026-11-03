from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    
    class Rol(models.TextChoices):
        CLIENTE = 'cliente', 'Cliente'
        COCINERO = 'cocinero', 'Cocinero'
        DUENA = 'duena', 'Dueña'

    
    rol = models.CharField(max_length=10, choices=Rol.choices, default=Rol.CLIENTE)
    telefono = models.CharField(max_length=15, blank=True)
    email = models.EmailField(unique=True)

    
    def es_cliente(self):
        return self.rol == self.Rol.CLIENTE

    def es_cocinero(self):
        return self.rol == self.Rol.COCINERO

    def es_duena(self):
        return self.rol == self.Rol.DUENA

    
    def __str__(self):
        return f'{self.username} ({self.get_rol_display()})'