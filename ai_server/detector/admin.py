from django.contrib import admin
from detector.models import ImageModel

# Register your models here.
@admin.register(ImageModel)
class ImageModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'image','detections', 'created_at')