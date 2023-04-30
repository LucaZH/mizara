import cpuinfo, mimetypes, platform, os

from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Transfer, UnauthorisedDirectory
from .serializers import SerializerUser, TransferSerializer, UnauthorisedDirectorySerializer, fileSerializer

class UserListCreateAPIView(APIView):
    def post(self, request):
        userserializer = SerializerUser(data=request.data)

        if userserializer.is_valid():
            if User.objects.filter(username=userserializer.validated_data["username"]).exists():
                return Response({"response":"this username is already used"}, status=status.HTTP_400_BAD_REQUEST)
            userserializer.save()
            return Response({"response": "user successfull added"}, status=status.HTTP_201_CREATED)

        return Response(userserializer.errors, status=status.HTTP_403_FORBIDDEN)
    
    def get(self, request):
        pk=request.user.id
        user = User.objects.filter(id=pk)
        if user.exists():
            serializer = SerializerUser(user)
            return Response(serializer.data)   
        
        return Response(status=status.HTTP_404_NOT_FOUND)

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

    def post(self, request):
        
        serializer = fileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FilesView(APIView):

    def classify_file(self,file_path):
        file_types = {
            "image": ["3dm", "3ds", "ai", "bmp", "dds", "dwg", "dxf", "gif", "jpg", "png", "svg", "tif"],
            "video": ["3g2", "3gp", "aaf", "asf", "avchd", "avi", "drc", "f4v", "f4p", "f4a", "f4b", "flv", "m2v", "m4p", "m4v", "mkv", "mng", "mov", "mp2", "mp4", "mpe", "mpeg", "mpg", "mpv", "mxf", "nsv", "ogv", "qt", "rm", "rmvb", "roq", "svi", "vob", "webm", "wmv", "yuv"],
            "audio": ["aac", "ape", "aiff", "au", "flac", "gsm", "it", "m3u", "m4a", "mid", "mod", "mp3", "mpa", "pls", "ra", "s3m", "sid", "wav", "wma", "xm"],
            "document": ["azw", "azw1", "azw3", "azw4", "azw6", "cbr", "cbz", "doc", "docx", "epub", "odt", "pages", "pdf", "rtf", "tex", "txt"],
            "archive": ["7z", "a", "apk", "ar", "bz2", "cab", "cpio", "deb", "dmg", "egg", "gz", "iso", "jar", "lha", "lz", "lzma", "lzo", "pkg", "rar", "rpm", "s7z", "shar", "sit", "tar", "tbz2", "tgz", "tlz", "txz", "war", "xap", "xz", "z", "zip"],
            }

        file_name, file_ext = os.path.splitext(file_path)
        file_ext = file_ext[1:].lower()

        for file_type, extensions in file_types.items():
            if file_ext in extensions:
                return file_type
        return "other"

    def get(self, request, folder):

        lang = os.getenv('LANG').split("_")[0]
        folders = {
            'Documents': {'en': 'Documents', 'fr': 'Documents'},
            'Music': {'en': 'Music', 'fr': 'Musique'},
            'Videos': {'en': 'Videos', 'fr': 'Vidéos'},
            'Pictures': {'en': 'Pictures', 'fr': 'Images'},
            'Downloads': {'en': 'Downloads', 'fr': 'Téléchargements'}
        }
        if folder not in folders:
            return Response({"error": "Invalid filetype name."}, status=status.HTTP_400_BAD_REQUEST)
        name = folders[folder][lang]
        path = os.path.join(os.path.expanduser("~"), name)
        
        if not os.path.exists(path):
            return Response({"error": f"{name} folder does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        result = []
        for root, dirs, files in os.walk(path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                file_ext = os.path.splitext(file_path)[1].lower()[1:]
                file_size = round(os.path.getsize(file_path) / 1024 / 1024 , 2)
                item = {
                    "name": file_name,
                    "extension": file_ext,
                    "path": file_path,
                    "size": file_size,
                }
                result.append(item)
        result.sort(key=lambda x: x['name'])
        
        return Response(result)

class DirectoryListAPIView(APIView):

    SIZE_UNIT = 1024
    
    def is_directory_unauthorised(self, directory_path):
        unauthorised_directories = [dir.directory_path for dir in UnauthorisedDirectory.objects.all()]
        for unauthorised_dir in unauthorised_directories:
            if directory_path.startswith(unauthorised_dir):
                return True
        return False
    
    def post(self, request):
        path = request.data.get('path')
        resp = []
        
        if not os.path.exists(path):
            return Response("No such files or directory", status=status.HTTP_400_BAD_REQUEST)

        if self.is_directory_unauthorised(path):
            return Response({"message": "Access to this directory is not allowed."}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            entries = os.scandir(path)
        except OSError:
            return Response("Error reading directory", status=status.HTTP_400_BAD_REQUEST)

        for entry in entries:
            if entry.is_dir():
                entry_type = "folder"
                extension = ""
            else:
                entry_type = "file"
                extension = entry.path.split(".")[-1]
            size = round(os.path.getsize(entry) / self.SIZE_UNIT ** 2, 4)
            resp.append({
                "name": entry.name,
                "type": entry_type,
                "extension": extension,
                "path": entry.path,
                "size": size
            })
            
        resp.sort(key=lambda x: x['name'])
        return Response(resp)

class DownloadAPIView(APIView):

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    
    def post(self,request):
        file_path = request.data.get('file_path')
        # user = request.user
        # user_instance = get_object_or_404(User, id=user.id)
        # transfer = Transfer.objects.create(downloader=user_instance, file_path=file_path)
        if not file_path or not os.path.exists(file_path):
            return Response("File not found.", status=status.HTTP_404_NOT_FOUND)
        
        mime_type, encoding = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = 'application/octet-stream'
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type=mime_type)
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(os.path.basename(file_path))
            return response

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

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        file_path = request.data.get('file_path')
        if not file_path or not os.path.exists(file_path):
            raise Http404
        with open(file_path, 'rb') as file:
            file_content = file.read()
        content_type, encoding = mimetypes.guess_type(file_path)
        response = HttpResponse(file_content, content_type=content_type)
        response['Content-Disposition'] = 'inline; filename="{}"'.format(file_path.split('/')[-1])
        return response

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
                    'Total size' : round(partition_info.total  / (1024.0 ** 3),2),
                    'Used': round(partition_info.used / (1024.0 ** 3),2),
                    'Free': round(partition_info.free / (1024.0 ** 3),2),
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

class Sysinfo(APIView):

    def get(self,request):
        sysinfo={
            'OS': platform.platform(),
            # 'Processor': platform.processor(),
            'cpu': cpuinfo.get_cpu_info()['brand_raw'],
            'Pc-name': platform.node(),
            'archi': platform.machine(),
            'homedir': os.path.expanduser("~"),
            'username': os.path.expanduser("~").split("/")[-1]
        }
        return Response(sysinfo,status=status.HTTP_201_CREATED)