from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username','first_name', 'last_name', 'email', 'password')
        read_only_fields = ('id', )

        extra_kwargs = {
            'password':{
                'write_only': True,
                'min_length':8,
                'help_text':'A senha deve ter pelo menos 8 digitos'
            }
        }

    def create(self, validated_data)->User:
        new_user = User.objects.create_user(**validated_data)
        return new_user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        #instance.nascimento = validated_data.get('nascimento', instance.nascimento)
        instance.save()
        return instance
