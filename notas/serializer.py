from rest_framework import serializers

from .models import Notas


class NotasSerializer(serializers.ModelSerializer):
    dono = serializers.ReadOnlyField(source="dono.username")

    class Meta:
        model = Notas
        fields = "__all__"
        read_only_fields = ["id", "dono"]

        extra_kwargs = {
            "titulo": {"help_text": "O titulo da nota deve ter pelo menos 3 palavras para ser aceito"},
            "descricao": {"help_text": "A descrição não pode ter o mesmo conteúdo do título."},
            "status": {"help_text": "1-concluido / 2-Fazendo / 3-pendente"},
        }

    def validate_titulo(self, value):
        if len(value.split()) < 3:
            raise serializers.ValidationError("O titulo deve ter pelo menos 3 palavras")
        return value.title()

    def validate(self, data):

        titulo = data.get("titulo")
        descricao = data.get("descricao")

        if titulo and descricao:
            if titulo == descricao:
                raise serializers.ValidationError(
                    {"non_field_erros":"O titulo não pode ser igual a descrição da nota."}
                )
            return data
        return data
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)