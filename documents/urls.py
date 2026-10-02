from django.urls import path
from .views import DocumentUploadVIew

urlpatterns = [
    path("upload/",DocumentUploadVIew.as_view(),name="document-upload")
]
