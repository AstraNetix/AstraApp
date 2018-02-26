from django.contrib.auth import get_user_model, login, logout
from api.models.device import Device
from api.serializers.user import (
    UserIdentificationSerializer,
    UserLoginSerializer,
    UserPasswordSerializer,
    UserBasicSerializer,
    UserICOKYCSerializer,
    UserBalanceSerializer,
    UserRelationalSerializer
)
from api.models.user_exceptions import *
from api.models.device_exceptions import *
from api.permissions import SuperUserPermission

from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import status

from rest_framework.decorators import detail_route, list_route  
from rest_framework.response import Response

User = get_user_model()

class UserIDViewSet(viewsets.ModelViewSet):
    serializer_class = UserIdentificationSerializer

    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserPermission]

    @list_route(methods=['patch'])
    def set_user_verified(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.exists():
            user = User.objects.get(email=serializer.data['email'])
            user.set_email_valid()
            return Response({'success': "User successfully email verified"}, 
                status=status.HTTP_200_OK)
        else: 
            return Response(serializer.email_error, 
                status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['get'])
    def user_valid_for_sale(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.exists():
            user = User.objects.get(email=serializer.data['email'])
            return Response({'result': user.boolean_token_auth()}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.email_error, 
                status=status.HTTP_400_BAD_REQUEST)


    @list_route(methods=['patch'])
    def request_password_reset(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.exists():
            user = User.objects.get(email=serializer.data['email'])
            user.reset_password_email()
            return Response({'success': "Password reset email successfully sent"})
        else: 
            return Response(serializer.email_error, 
                status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['patch'])     
    def logout_user(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.exists():
            logout(request)
            return Response({'success': "User successfully logged out"})
        else: 
            return Response(serializer.email_error, 
                status=status.HTTP_400_BAD_REQUEST)


class UserBasicViewSet(viewsets.ModelViewSet):
    serializer_class = UserBasicSerializer

    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserPermission]

    @list_route(methods=['post'])
    def create_user(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            try:
                serializer.create(serializer.validated_data)
                return Response({"success", "User successfully created"},
                    status=status.HTTP_201_CREATED)
            except CreationError as ce:
                return Response({"failure", str(ce)},
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginViewSet(viewsets.ModelViewSet):
    serializer_class = UserLoginSerializer
    serializer_data_class = UserICOKYCSerializer
    serializer_balance_class = UserBalanceSerializer
    
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserPermission]

    @list_route(methods=['patch'])
    def login_user(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.exists():
            try:
                user = User.authenticate(serializer.data['email'], 
                    serializer.data['password'])
                user.login()
                return Response({
                        'success': "User successfully logged in", 
                        'data': self.serializer_data_class(user).data,
                        'balance': self.serializer_balance_class(user).data,
                    }, status=status.HTTP_201_CREATED)
            except AuthenticationError as ae:
                return Response({'failure': str(ae)}, 
                    status=status.HTTP_401_UNAUTHORIZED)
        else: 
            return Response(serializer.email_error, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordViewSet(viewsets.ViewSet):
    serializer_class = UserPasswordSerializer

    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserPermission]

    @list_route(methods=['patch'])
    def reset_password(self, request, pk=None):
        serializer = self.serializer_class(data=request.data, partial=True)

        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.validated_data['email'])
                user.reset_password(serializer.validated_data['new_password'])
                return Response({'success': "User password successfully reset"})
            except PasswordChangeError as pc:
                return Response({'failure': str(pc)},
                    status=status.HTTP_400_BAD_REQUEST)
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['patch'])
    def change_password(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.validated_data['email'])
                user.change_password(serializer.validated_data['old_password'], 
                    serializer.validated_data['new_password'])
                return Response({'success': "User password successfully reset"})
            except PasswordChangeError as pc:
                return Response({'failure': str(pc)},
                    status=status.HTTP_400_BAD_REQUEST)
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            
class UserICOKYCViewSet(viewsets.ViewSet):
    serializer_class = UserICOKYCSerializer

    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserPermission]

    @list_route(methods=['post'])
    def add_ICOKYC_data(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data.pop('email'))
            for key, value in serializer.validated_data.items():   
                setattr(user, key, value)
            return Response({'success': "User password successfully reset"})
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

class UserBalanceViewSet(viewsets.ModelViewSet):
    serializer_class = UserBalanceSerializer
    
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserPermission]

    @detail_route(methods=['patch'])
    def add_star(self, request, pk=None):
        return self.add_tokens(User.add_star_tokens, 'star', request)

    @detail_route(methods=['patch'])
    def add_usd(self, request, pk=None):
        return self.add_tokens(User.add_usd, 'star', request)

    @detail_route(methods=['patch'])
    def add_btc(self, request, pk=None):
        return self.add_tokens(User.add_bitcoin, 'star', request)

    @detail_route(methods=['patch'])
    def add_ether(self, request, pk=None):
        return self.add_tokens(User.add_ether, 'star', request)

    def add_tokens(self, func, token_type, request):
        serializer = UserIdentificationSerializer(data=request.data)

        if serializer.exists():
            try: 
                user = User.objects.get(email=serializer.data['email'])
                func(user, serializer.data[token_type]) 
                return Response({'success': '{0} added'.format(token_type)})
            except TokenICOKYCError as tik:
                return Response({'failure': str(tik)}, 
                    status=status.HTTP_412_PRECONDITION_FAILED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

class UserRelationalViewSet(viewsets.ViewSet):
    serializer_class = UserRelationalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserPermission]

    @list_route(methods=['patch'])
    def start_project(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.exists():
            try:
                user = User.objects.get(email=serializer.data['email'])
                device = User.devices.get(pk=serializer.data['device_id'])
                device.start_project(pk=serializer.data['project_id'])
                return Response({'success': "Project successfully started"})
            except DeviceClientError as dce:
                return Response({'failure': str(dce)}, 
                    status=status.HTTP_400_BAD_REQUEST)
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['patch'])
    def stop_project(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.exists():
            try:
                user = User.objects.get(email=serializer.data['email'])
                device = User.devices.get(pk=serializer.data['device_id'])
                device.stop_project(pk=serializer.data['project_id'])

                return Response({'success': "Project successfully stopped"})
            except DeviceClientError as dce:
                return Response({'failure': str(dce)}, 
                    status=status.HTTP_400_BAD_REQUEST)
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




