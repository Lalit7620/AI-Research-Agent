from rest_framework import serializers
from .models import ResearchRequest


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