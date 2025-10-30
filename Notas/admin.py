from django.contrib import admin
from .models import Notas

@admin.register(Notas)
class AdminNotas(admin.ModelAdmin):
    list_display = ['dono','titulo','data_criacao']
    list_filter = ['dono', 'titulo']