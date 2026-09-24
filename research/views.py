from rest_framework import generics
from .models import ResearchRequest
from .serializers import ResearchRequestSerializers


class ResearchRequestCreateView(generics.CreateAPIView):
    queryset=ResearchRequest.objects.all()
    serializer_class=ResearchRequestSerializers
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)