from django.shortcuts import render
from rest_framework.generics import CreateAPIView,ListAPIView,DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import MultiPartParser,FormParser
from .services.ingestion import ingest_document
from .services.vector_store import delete_document_chunks

from .models import Document
from .serializers import DocumentSerializer



def document_dashboard(request):
    return render(
        request,
        "documents/dashboard.html"
    )

class DocumentUploadVIew(CreateAPIView):
    queryset=Document.objects.all()
    serializer_class=DocumentSerializer
    
    authentication_classes=[SessionAuthentication]
    permission_classes=[IsAuthenticated]
    
    parser_classes=[MultiPartParser,FormParser]
    
    def perform_create(self, serializer):
        document=serializer.save(user=self.request.user)
        
        ingest_document(document)
        
class DocumentListView(ListAPIView):
    serializer_class=DocumentSerializer
    authentication_classes=[SessionAuthentication]
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        return Document.objects.filter(
            user=self.request.user
        ).order_by("-uploaded_at")
        
class DocumentDeleteView(DestroyAPIView):
    serializer_class=DocumentSerializer
    authentication_classes=[SessionAuthentication]
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        return Document.objects.filter(
            user=self.request.user
        )
        
    def perform_destroy(self, instance):
        delete_document_chunks(
            instance.id
        )
        instance.file.delete(
            save=False
        )
        instance.delete()