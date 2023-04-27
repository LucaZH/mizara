from django.db import models
from django.contrib.auth.models import User

class File(models.Model):
    name = models.CharField(max_length=255)
    size = models.IntegerField()
    file_type = models.CharField(max_length=50)
    file = models.FileField(upload_to='files/')

class Transfer(models.Model):
    downloader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_files')
    date = models.DateTimeField(auto_now_add=True)
    file_path = models.ForeignKey(File, on_delete=models.CASCADE)


class UnauthorisedDirectory(models.Model):
    directory_path = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

