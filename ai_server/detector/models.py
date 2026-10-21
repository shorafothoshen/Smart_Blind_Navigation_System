from django.db import models

class ImageModel(models.Model):
    image = models.ImageField(upload_to='images/')
    detections = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}"