from django.urls import path
from .views import ObjectDetectionAPIView

urlpatterns = [
    path("detect/", ObjectDetectionAPIView.as_view(), name="detect"),
]
