from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    email = models.EmailField(unique=True)
    avatar = models.ImageField(
        upload_to="avatars/",
        default="avatars/default.png",
        help_text="Avatar do usuário",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"O usúario {self.username} cadastrado com sucesso"
