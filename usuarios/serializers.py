from rest_framework import serializers
from django.contrib.auth.models import User
from .models import PerfilUsuario, Rol

class RegistroSerializer(serializers.ModelSerializer):
    telefono = serializers.CharField(write_only=True)
    rol = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'telefono', 'rol']

    def create(self, validated_data):
        rol_nombre = validated_data.pop('rol')
        telefono = validated_data.pop('telefono')

        try:
            rol = Rol.objects.get(nombre=rol_nombre)
        except Rol.DoesNotExist:
            raise serializers.ValidationError({'rol': 'El rol especificado no existe'})

        user = User.objects.create_user(
            username=f"{validated_data['first_name']} {validated_data['last_name']}",
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        PerfilUsuario.objects.create(
            usuario=user,
            telefono=telefono,
            rol=rol
        )
        
        return user