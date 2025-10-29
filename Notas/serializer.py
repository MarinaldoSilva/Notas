from rest_framework import serializers
from .models import Notas


class NotasSerializer(serializers.ModelSerializer):
    dono = serializers.ReadOnlyField(source='dono.username')
    class Meta:
        model = Notas
        fields = '__all__'
        read_only_fields = ['id','dono']
