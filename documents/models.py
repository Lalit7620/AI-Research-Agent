from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    user=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="documents"
    )
    
    file=models.FileField(upload_to="documents/")
    uploaded_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.file.name