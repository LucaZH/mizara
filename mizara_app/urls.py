from django.urls import path
from .views import DirectoryListAPIView, UnauthorisedDirectoryDetail, UnauthorisedDirectoryList, fileUploadView, UserListCreateAPIView,DownloadAPIView,DiskAPIView,FileStreamingView
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('api/users/', UserListCreateAPIView.as_view()),
    path('api/users/<int:pk>/', UserListCreateAPIView.as_view()),
    path('api/token/', ObtainAuthToken.as_view()),
    path('api/upload/', fileUploadView.as_view()),
    path('api/directories/', DirectoryListAPIView.as_view()),
    path('api/download/', DownloadAPIView.as_view()),
    path('api/disk/',DiskAPIView.as_view()),
    path('api/unauthorised_directories/', UnauthorisedDirectoryList.as_view()),
    path('api/unauthorised_directories/<int:pk>/', UnauthorisedDirectoryDetail.as_view()),
    path('api/streaming/' , FileStreamingView.as_view())
]
