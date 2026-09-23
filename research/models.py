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
    
    created_at=