from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class ResearchRequest(models.Model):
    STATUS_CHOICES=[
        ("PENDING","Pending"),
        ("RESEARCHING","Researching"),
        ("COMPLETED","Completed"),
        ("FAILED","Failed"),
    ]
    
    user=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="research_requests"
    )
    
    query=models.TextField()
    
    status=models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )
    
    created_at=models.DateTimeField(auto_now_add=True)
    
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.query
    
class ResearchReport(models.Model):
    research_request=models.OneToOneField(
        ResearchRequest,
        on_delete=models.CASCADE,
        related_name="report"
    )
    
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Report for: {self.research_request.query}"