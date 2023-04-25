from rest_framework import serializers
from django.contrib.auth.models import User
from .models import File,UnauthorisedDirectory

class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255, write_only=True)
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user
class fileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
class UnauthorisedDirectorySerializer(serializers.ModelSerializer):
    class Meta:
        model= UnauthorisedDirectory
        fields = 'directory'