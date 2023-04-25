from django.urls import path
from .views import DirectoryListAPIView, FichierUploadView, UserListCreateAPIView,DownloadAPIView
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('api/users/', UserListCreateAPIView.as_view(), name='user_list_create'),
    path('api/users/<int:pk>/', UserListCreateAPIView.as_view(), name='user_detail'),
    path('api/token/', ObtainAuthToken.as_view()),
    path('api/upload/', FichierUploadView.as_view(), name='fichier_upload'),
    path('api/directories/<path:directory>/', DirectoryListAPIView.as_view(), ),
    path('api/download/<path:file_path>/', DownloadAPIView.as_view(), ),
]
