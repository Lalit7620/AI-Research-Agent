from rest_framework import serializers
from .models import ResearchRequest,ResearchReport


class ResearchRequestSerializers(serializers.ModelSerializer):
    class Meta:
        model=ResearchRequest
        fields=[
            "id",
            "query",
            "status",
            "created_at",
            "updated_at"
        ]
        
        read_only_fields=[
            "id",
            "status",
            "created_at",
            "updated_at"
        ]
        
        
class ResearchHistorySerializers(serializers.ModelSerializer):
    class Meta:
        model=ResearchRequest
        fields=[
            "id",
            "query",
            "status",
            "created_at",
            "updated_at"
        ]
        
class ResearchReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = ResearchReport
        fields = [
            "id",
            "content",
            "created_at",
            "updated_at"
        ]