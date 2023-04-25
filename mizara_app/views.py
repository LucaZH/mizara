import mimetypes
import os
from django.http import Http404,HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import FichierSerializer, UserSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Fichier
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class UserListCreateAPIView(APIView):
    def get(self, request,pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            if User.objects.filter(username=serializer.validated_data["username"]).exists():
                    return Response({"response":"this username is already used"}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"response":"user successfull added"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FichierUploadView(APIView):
    def post(self, request, format=None):
        serializer = FichierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class DirectoryListAPIView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request, directory):
        directories = []
        files = []
        for entry in os.scandir(directory):
            if entry.is_dir():
                directories.append(entry.name)
            else:
                files.append(entry.name)
        return Response({"directories": directories, "files": files})

class DownloadAPIView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request, file_path):
        if not os.path.exists(file_path):
            raise Http404
        mime_type, encoding = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = 'application/octet-stream'
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type=mime_type)
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(os.path.basename(file_path))
            return response