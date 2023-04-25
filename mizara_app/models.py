from django.db import models
from django.contrib.auth.models import User

class File(models.Model):
    name = models.CharField(max_length=255)
    size = models.IntegerField()
    file_type = models.CharField(max_length=50)
    file = models.FileField(upload_to='files/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')

class Transfer(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_files')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_files')
    date = models.DateTimeField(auto_now_add=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE)

class TransferHistory(models.Model):
    transfer = models.ForeignKey(Transfer, on_delete=models.CASCADE, related_name='history')
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)



class UnauthorisedDirectory(models.Model):
    directory = models.CharField(max_length=255)
    def __str__(self):
        return self.directory

