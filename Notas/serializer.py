from rest_framework import serializers
from .models import Notas
from datetime import datetime

class NotasSerializer(serializers.ModelSerializer):
    dono = serializers.ReadOnlyField(source='dono.username')
    class Meta:
        model = Notas
        fields = '__all__'
        read_only_fields = ['id','dono']

    def validate_titulo(self, value):
        min_palavras = 3
        if len(value.split()) < min_palavras:
            raise serializers.ValidationError(f"O titulo deve ter pelo menos {min_palavras} palavras")
        return value.title()
    
    def validate(self, data):
        titulo = data['titulo']
        descricao = data['descricao']

        if titulo and descricao:
            if titulo.strip().lower() == descricao.strip().lower():
                raise serializers.ValidationError("O titulo não pode ser igual a descrição da atividade.")
            return data
        
    def update(self, instance, validated_data):
        if 'titulo' in validated_data and instance.titulo != validated_data['titulo']:
            data_update_title = datetime.now().strftime("%d/%m/%y")
            validated_data['titulo'] = f"{validated_data['titulo']} - Atualizado em {data_update_title}"
            return super().update(instance, validated_data)
        return instance