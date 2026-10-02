from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import MultiPartParser,FormParser

from .models import Document
from .serializers import DocumentSerializer


class DocumentUploadVIew(CreateAPIView):
    queryset=Document.objects.all()
    serializer_class=DocumentSerializer
    
    authentication_classes=[SessionAuthentication]
    permission_classes=[IsAuthenticated]
    
    parser_classes=[MultiPartParser,FormParser]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)