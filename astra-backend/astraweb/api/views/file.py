from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import status

from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.decorators import detail_route, list_route  
from rest_framework.response import Response


from api.serializers.file import FileUploadSerializer
from api.models.file import File
from api.permissions import APIUserPermission

class FileUploadViewSet(viewsets.ModelViewSet):
    serializer_class = FileUploadSerializer
    queryset = File.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, APIUserPermission]
    parser_classes = (MultiPartParser, FormParser,)
    
    def perform_create(self, request, pk=None):
        serializer = self.serializer_class(data=self.request.data)
        
        if serializer.exists():
            serializer.create(serializer.validated_data)
            return Response({'success': 'File successfully uploaded'}, 
                    status=status.HTTP_200_OK)
        else:
            return Response({'email': ['Email does not exist.']}, 
                    status=status.HTTP_400_BAD_REQUEST)