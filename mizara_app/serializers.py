from rest_framework import serializers
from django.contrib.auth.models import User
from .models import File, Transfer,UnauthorisedDirectory

class SerializerUser(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=255, write_only=True)
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class fileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

class UnauthorisedDirectorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UnauthorisedDirectory
        fields = ['directory_path', 'created_at']
        read_only_fields = ['created_at']

class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'