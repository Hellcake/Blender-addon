from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SceneSave

class SaveSceneView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            file_path = request.data.get('file_path')
            
            if not username or not file_path:
                return Response(
                    {'error': 'username and file_path are required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            scene_save = SceneSave.objects.create(
                username=username,
                file_path=file_path
            )

            return Response({
                'id': scene_save.id,
                'username': scene_save.username,
                'timestamp': scene_save.timestamp,
                'file_path': scene_save.file_path
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )