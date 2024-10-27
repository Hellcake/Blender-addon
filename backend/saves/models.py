from django.db import models

class SceneSave(models.Model):
    username = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    file_path = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.username} - {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']