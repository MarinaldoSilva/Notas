from django.db import models
from django.conf import settings


class Notas(models.Model):

    class StatusNotas(models.IntegerChoices):
        CONCLUIDO = 1, "Concluido"
        FAZENDO = 2, "Fazendo"
        PENDENTE = 3, "Pendente"

    dono = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200, null=False, blank=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=StatusNotas.choices, default=StatusNotas.PENDENTE)

    def __str__(self):
        return f"{self.titulo}"