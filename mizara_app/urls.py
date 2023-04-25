from django.urls import path
from .views import DirectoryListAPIView, fileUploadView, UserListCreateAPIView,DownloadAPIView,DiskAPIView
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('api/users/', UserListCreateAPIView.as_view),
    path('api/users/<int:pk>/', UserListCreateAPIView.as_view()),
    path('api/token/', ObtainAuthToken.as_view()),
    path('api/upload/', fileUploadView.as_view()),
    path('api/directories/<path:directory>/', DirectoryListAPIView.as_view()),
    path('api/download/<path:file_path>/', DownloadAPIView.as_view()),
    path('api/disk/',DiskAPIView.as_view()),
]
