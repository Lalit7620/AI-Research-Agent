from django.urls import path
from .views import DocumentUploadVIew,DocumentListView,DocumentDeleteView,document_dashboard

urlpatterns = [
    path(
    "documents/",
    document_dashboard,
    name="documents-dashboard"
    ),
    path("upload/",DocumentUploadVIew.as_view(),name="document-upload"),
    path(
        "",
        DocumentListView.as_view(),
        name="document-list"
    ),
    path(
        "<int:pk>/",
        DocumentDeleteView.as_view(),
        name="document-delete"
    ),
]
