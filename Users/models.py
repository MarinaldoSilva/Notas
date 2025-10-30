from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    #nascimento = models.DateField(null=False, blank=False, help_text="Data de nascimento.")   
    eamil = models.EmailField(unique=True)
    #avatar = models.ImageField(upload_to='foto-user', blank=True, null=True)
    def __str__(self):
        return f"O usúario {self.username} cadastrado com sucesso"
