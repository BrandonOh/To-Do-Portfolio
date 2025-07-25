from django.db import models
from django.utils import timezone

# Model for the ToDo
class TodoItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    session_key = models.CharField(max_length=40)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['session_key']),
        ]

    def __str__(self):
        return f"{self.title} ({self.session_key[:8]}...)"