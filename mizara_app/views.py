import mimetypes,os,psutil
from django.shortcuts import get_object_or_404
from .serializers import SerializerUser, TransferSerializer, UnauthorisedDirectorySerializer,fileSerializer
from .models import UnauthorisedDirectory
from django.http import Http404,HttpResponse
from rest_framework.exceptions import ValidationError
from rest_framework import status,generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from .models import Transfer
class UserListCreateAPIView(APIView):
    def post(self, request):
        userserializer = SerializerUser(data=request.data)

        if userserializer.is_valid():
            if User.objects.filter(username=userserializer.validated_data["username"]).exists():
                return Response({"response":"this username is already used"}, status=status.HTTP_400_BAD_REQUEST)
            userserializer.save()
            return Response({"response": "user successfull added"}, status=status.HTTP_201_CREATED)

        return Response(userserializer.errors, status=status.HTTP_403_FORBIDDEN)
    def get(self, request,pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SerializerUser(user)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SerializerUser(user, data=request.data)
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

class fileUploadView(APIView):

    def post(self, request, format=None):
        serializer = fileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DirectoryListAPIView(APIView):

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        directories = []
        files = []
        directory = self.request.query_params.get('dir')
        filter = request.GET.get('filter', '')
        
        try :
            unauthorised_directories = [dir.directory_path for dir in UnauthorisedDirectory.objects.all()]
            
            for unauthorised_dir in unauthorised_directories:
                if directory.startswith(unauthorised_dir):
                    return Response({"message": "Access to this directory is not allowed."}, status=status.HTTP_403_FORBIDDEN)
            
            for entry in os.scandir(directory):
                if entry.is_dir():
                    
                    directories.append(entry.name)
                else:
                    file_size = round(os.path.getsize(entry)/ 1024 / 1024,4)
                    files.append({'file_name' : entry.name,
                                  'file_size': f'{file_size} MB'
                                  })
            directories = sorted(directories)
            if filter=="name":
                files = sorted(files, key=lambda f: f['file_name'])
            elif filter =="ext":
                files = sorted(files, key=lambda f: (os.path.splitext(f['file_name'])[1], f['file_name']))
            else:
                files = sorted(files, key=lambda f: f['file_name'])

            return Response({"directories": directories, "files": files})
        except:
            return Response(f"No such files no directory {directory}", status=status.HTTP_400_BAD_REQUEST)

class DownloadAPIView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        file_path = self.request.query_params.get('file_path')
        user = request.user
        user_instance = get_object_or_404(User, id=user.id)
        transfer = Transfer.objects.create(downloader=user_instance, file_path=file_path)
        if not file_path or not os.path.exists(file_path):
            raise Http404
        mime_type, encoding = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = 'application/octet-stream'
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type=mime_type)
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(os.path.basename(file_path))
            return response

class FileStreamingView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        file_path = self.request.query_params.get('file_path')
        if not file_path or not os.path.exists(file_path):
            raise Http404
        with open(file_path, 'rb') as file:
            file_content = file.read()
        content_type, encoding = mimetypes.guess_type(file_path)
        response = HttpResponse(file_content, content_type=content_type)
        response['Content-Disposition'] = 'inline; filename="{}"'.format(file_path.split('/')[-1])
        return response

class DiskAPIView(APIView):

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        partitions = psutil.disk_partitions(all=True)
        part = []
        for partition in partitions:
            if partition.device.startswith('/dev'):
                partition_info = psutil.disk_usage(partition.mountpoint)
                part.append({
                    'Device': partition.device,
                    'Mountpoint': partition.mountpoint,
                    'File systeme type': partition.fstype,
                    'Total size' : f'{round(partition_info.total  / (1024.0 ** 3),2)} GB',
                    'Used': f'{round(partition_info.used / (1024.0 ** 3),2)} GB',
                    'Free': f'{round(partition_info.free / (1024.0 ** 3),2)} GB',
                    'Percentage Used' : partition_info.percent
                })
        return Response(part,status=status.HTTP_201_CREATED)

class UnauthorisedDirectoryList(APIView):
    
    def get(self, request):
        directories = UnauthorisedDirectory.objects.all()
        serializer = UnauthorisedDirectorySerializer(directories, many=True)
        return Response(serializer.data)

    def post(self, request):
        directory_path = request.data.get('directory_path')
        if UnauthorisedDirectory.objects.filter(directory_path=directory_path).exists():
            raise ValidationError('Directory already exists.')
        serializer = UnauthorisedDirectorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UnauthorisedDirectoryDetail(APIView):

    def get_object(self, pk):
        try:
            return UnauthorisedDirectory.objects.get(pk=pk)
        except UnauthorisedDirectory.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        directory = self.get_object(pk)
        serializer = UnauthorisedDirectorySerializer(directory)
        return Response(serializer.data)

    def put(self, request, pk):
        directory = self.get_object(pk)
        serializer = UnauthorisedDirectorySerializer(directory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        directory = self.get_object(pk)
        directory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TransferList(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        Transfers = Transfer.objects.all()
        serializer = TransferSerializer(Transfers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)