from api.models.social_media_post import SocialMediaPost
from api.serializers.social_media_post import SocialMediaPostCreateSerializer, SocialMediaPostIDSerializer
from api.exceptions.user_exceptions import AuthenticationError

from api.permissions import SuperUserPermission

from rest_framework.decorators import detail_route, list_route  
from rest_framework.response import Response

from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import status

class SocialMediaPostViewSet(viewsets.ModelViewSet):
    serializer_class = SocialMediaPostCreateSerializer

    queryset = SocialMediaPost.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserPermission]

    @list_route(methods=['post'])
    def create_post(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            try:
                serializer.create()
                return Response({'success': "Social media post(s) successfully created"}, 
                    status=status.HTTP_200_OK)
            except AuthenticationError as ae: 
                return Response(ae.errors, status=status.HTTP_400_BAD_REQUEST)
        else: 
            return Response({'failure': serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST)
    
    @list_route(methods=['patch'])
    def validate(self, request, pk=None):
        serializer = SocialMediaPostIDSerializer(data=request.data)
        user = User.objects.get(email=serializer.validated_data['email'])

        if serializer.is_valid():
            post = SocialMediaPost.objects.get(
                date = SocialMediaPostCreateSerializer.convert_date(
                    serializer.validated_data['str_date']), 
                user = user,
            )
            post.verify()
            return Response({'success': "Social media post(s) successfully validated"}, status=status.HTTP_200_OK)
        else: 
            return Response({'failure': serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST)
