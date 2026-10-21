from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

from .serializers import ImageUploadSerializer
from .models import ImageModel
from .yolo_model import detect_objects

class ObjectDetectionAPIView(APIView):

    def get(self, request):
        latest = ImageModel.objects.last()

        if not latest:
            return Response({
                "success": True,
                "message": "No data found",
                "detections": []
            })

        return Response({
            "success": True,
            "image": latest.image.url if latest.image else None,
            "detections": latest.detections
        })

    def post(self, request):
        serializer = ImageUploadSerializer(data=request.data)

        if serializer.is_valid():
            image = serializer.validated_data['image']

            obj = ImageModel.objects.create(image=image)

            img_path = obj.image.path

            try:
                # YOLO detection
                results = detect_objects(img_path)

                # save detections in DB
                obj.detections = results
                obj.save()

                return Response({
                    "success": True,
                    "id": obj.id,
                    "detections": results
                })

            except Exception as e:
                return Response({
                    "success": False,
                    "error": str(e)
                }, status=500)

        return Response(serializer.errors, status=400)