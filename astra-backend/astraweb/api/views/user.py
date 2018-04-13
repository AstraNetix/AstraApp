from django.contrib.auth import get_user_model, login, logout
from api.models.device import Device
from api.models.file import File

from api.serializers.user import (
    UserIdentificationSerializer,
    UserLoginSerializer,
    UserPasswordSerializer,
    UserBasicSerializer,
    UserUpdateSerializer,
    UserICOKYCSerializer,
    UserBalanceSerializer,
    UserRelationalSerializer
)
from api.exceptions.user_exceptions import *
from api.exceptions.device_exceptions import *
from api.permissions import APIUserPermission

from api.sales.promo_sale import PromoSale

from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import status

from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route  

User = get_user_model()

class UserIDViewSet(viewsets.ModelViewSet):
    serializer_class = UserIdentificationSerializer

    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, APIUserPermission]

    @list_route(methods=['patch'])
    def set_user_verified(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.exists():
            user = User.objects.get(email=serializer.data['email'])
            user.set_email_valid()
            PromoSale.registered(user)
            return Response({'success': "User successfully email verified"}, 
                status=status.HTTP_200_OK)
        else: 
            return Response(serializer.email_error, 
                status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['patch'])
    def user_valid_for_sale(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.exists():
            user = User.objects.get(email=serializer.data['email'])
            return Response({'result': user.boolean_token_auth()}, 
            status=status.HTTP_200_OK)
        else:
            return Response(serializer.email_error, 
                status=status.HTTP_400_BAD_REQUEST)


    @list_route(methods=['patch'])
    def request_password_reset(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.exists():
            user = User.objects.get(email=serializer.data['email'])
            user.reset_password_email()
            return Response({'success': "Password reset email successfully sent"},
                status=status.HTTP_200_OK)
        else: 
            return Response(serializer.email_error, 
                status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['patch'])     
    def logout_user(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.exists():
            logout(request)
            return Response({'success': "User successfully logged out"}, 
                status=status.HTTP_200_OK)
        else: 
            return Response(serializer.email_error, 
                status=status.HTTP_400_BAD_REQUEST)
    
    @list_route(methods=['patch'])
    def get_name(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.exists():
            user = User.objects.get(email=serializer.data['email'])
            return Response({ 'name' : str(user) }, status=status.HTTP_200_OK)
        else: 
            return Response(serializer.email_error,
                            status=status.HTTP_400_BAD_REQUEST)
    
    @list_route(methods=['patch'])
    def get_referrals(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.exists():
            user = User.objects.get(email=serializer.data['email'])
            return Response({ 
                'referral_code'     : user.referral_code,
                'referral_count'    : user.referral_count(),
            }, status=status.HTTP_200_OK)
        else: 
            return Response(serializer.email_error,
                            status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['patch'])
    def get_ICO_KYC(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.exists():
            user = User.objects.get(email=serializer.data['email'])
            referrer = user.referral_user
            referral_code = referrer.referral_code if referrer else ""

            return Response({
                'first_name'        :   user.first_name         or "",
                'middle_name'       :   user.middle_name        or "",
                'last_name'         :   user.last_name          or "",
                'street_addr1'      :   user.street_addr1       or "",
                'street_addr2'      :   user.street_addr2       or "",
                'city'              :   user.city               or "",
                'state'             :   user.state              or "",
                'country'           :   user.country            or "",
                'zip_code'          :   user.zip_code           or "",
                'phone_number'      :   user.phone_number       or "",
                'ether_addr'        :   user.ether_addr         or "",
                'ether_part_amount' :   user.ether_part_amount  or "",
                'referral_type'     :   user.referral_type      or "",
                'referral_code'     :   referral_code,
                'whitepaper'        :   user.whitepaper, 
                'token_sale'        :   user.token_sale,         
                'data_protection'   :   user.data_protection,    
            }, status=status.HTTP_200_OK)
        else: 
            return Response(serializer.email_error,
                            status=status.HTTP_400_BAD_REQUEST)
    
    @list_route(methods=['patch'])
    def get_balance(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.exists(): 
            user = User.objects.get(email=serializer.data['email'])
            return Response({
                'bitcoin'       :   user.bitcoin_balance,
                'ether'         :   user.star_balance,
                'usd'           :   user.usd_balance,
                'star'          :   user.star_balance,
                'bonus_star'    :   user.bonus_star_balance,
            }, status=status.HTTP_200_OK)
        else: 
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['patch'])
    def get_file_names(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.exists(): 
            user = User.objects.get(email=serializer.data['email'])
            id_file = File.id_file(user)
            selfie = File.selfie(user)

            return Response({
                'selfie'    :   selfie.name if selfie else '',
                'id_file'   :   id_file.name if id_file else '',
            }, status=status.HTTP_200_OK)
        else: 
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['patch'])
    def delete_user(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.exists():
            user = User.objects.get(email=serializer.data['email'])
            user.delete()
            return Response({"success": "User successfully deleted"},
                    status=status.HTTP_200_OK)
        else: 
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['patch'])
    def get_devices(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.exists():
            user = User.objects.get(email=serializer.data['email'])
            return Response({device.uid : str(device) for device in user.devices.all()},
                    status=status.HTTP_200_OK)
        else: 
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

class UserBasicViewSet(viewsets.ModelViewSet):
    serializer_class = UserBasicSerializer

    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, APIUserPermission]

    @list_route(methods=['post'])
    def create_user(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            try:
                serializer.create(serializer.validated_data)
                return Response({"success": "User successfully created"},
                    status=status.HTTP_201_CREATED)
            except (CreationError, KeyError) as error:
                return Response(error.errors,
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserUpdateViewSet(viewsets.ModelViewSet):
    serializer_class = UserUpdateSerializer

    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, APIUserPermission]

    @list_route(methods=['patch'])
    def update_user(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.exists():
            try:
                serializer.update(serializer.validated_data)
                return Response({"success": "User successfully updated"},
                    status=status.HTTP_201_CREATED)
            except (CreationError, AuthenticationError) as ce:
                return Response(ce.errors,
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginViewSet(viewsets.ModelViewSet):
    serializer_class = UserLoginSerializer
    serializer_data_class = UserICOKYCSerializer
    serializer_balance_class = UserBalanceSerializer
    
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, APIUserPermission]

    @list_route(methods=['patch'])
    def login_user(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.exists():
            try:
                user = User.login(serializer.data['email'], 
                    serializer.data['password'])
                return Response({
                        'success': "Successfully logged in", 
                        'data': self.serializer_data_class(user).data,
                        'balance': self.serializer_balance_class(user).data,
                    }, status=status.HTTP_200_OK)
            except AuthenticationError as ae:
                return Response(ae.errors, 
                    status=status.HTTP_401_UNAUTHORIZED)
        else: 
            return Response(serializer.email_error, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordViewSet(viewsets.ViewSet):
    serializer_class = UserPasswordSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, APIUserPermission]

    @list_route(methods=['patch'])
    def reset_password(self, request, pk=None):
        try:
            serializer = self.serializer_class(data=request.data, partial=True)

            if serializer.is_valid():
                try:
                    user = User.objects.get(email=serializer.validated_data['email'])
                    user.reset_password(serializer.validated_data['new_password'])
                    return Response({'success': "Password successfully reset. Check your inbox!"}, 
                        status=status.HTTP_200_OK)
                except PasswordChangeError as pc:
                    return Response(pc.errors,
                        status=status.HTTP_400_BAD_REQUEST)
            else: 
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
                return Response({'email': ['This field must not be blank']},
                    status=status.HTTP_400_BAD_REQUEST) 

    @list_route(methods=['patch'])
    def change_password(self, request, pk=None):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                user = User.objects.get(email=serializer.validated_data['email'])
                user.change_password(serializer.validated_data['old_password'], 
                    serializer.validated_data['new_password'])
                return Response({'success': "Password successfully changed"}, 
                    status=status.HTTP_200_OK)
            else: 
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PasswordChangeError as pc:
            return Response(pc.errors,
                status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
                return Response(AuthenticationError.MISSING_FIELDS,
                    status=status.HTTP_400_BAD_REQUEST)
            
            
class UserICOKYCViewSet(viewsets.ViewSet):
    serializer_class = UserICOKYCSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, APIUserPermission]

    @list_route(methods=['patch'])
    def add_ICOKYC_data(self, request, pk=None):
        try:
            serializer = self.serializer_class(data=request.data)
        
            if serializer.exists():
                serializer.add_icokyc()
                if any(serializer.check_errors):
                    return Response(serializer.check_errors, 
                        status=status.HTTP_200_OK) 
                return Response({'success': "ICOKYC data successfully set"}, 
                    status=status.HTTP_200_OK) 
            else: 
                return Response(serializer.errors, 
                    status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'email': ["This field must not be blank"]}, 
                    status=status.HTTP_400_BAD_REQUEST)
        except ReferralError as re:
            return Response(re.errors,
                    status=status.HTTP_400_BAD_REQUEST)

class UserBalanceViewSet(viewsets.ViewSet):
    serializer_class = UserBalanceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, APIUserPermission]

    @list_route(methods=['patch'])
    def add_star(self, request, pk=None):
        return self.add_tokens(User.add_star_tokens, 'star', request)

    @list_route(methods=['patch'])
    def add_usd(self, request, pk=None):
        return self.add_tokens(User.add_usd, 'usd', request)

    @list_route(methods=['patch'])
    def add_btc(self, request, pk=None):
        return self.add_tokens(User.add_bitcoin, 'bitcoin', request)

    @list_route(methods=['patch'])
    def add_ether(self, request, pk=None):
        return self.add_tokens(User.add_ether, 'ether', request)

    def add_tokens(self, token_func, token_type, request):
        try: 
            serializer = self.serializer_class(data=request.data, partial=True)
            
            if serializer.exists():
                user = User.objects.get(email=serializer.data['email'])
                if token_type not in serializer.data:
                    return Response({token_type: ["This field must not be blank"]}, 
                        status=status.HTTP_400_BAD_REQUEST)
                token_func(user, serializer.data[token_type]) 
                return Response({'success': '{0} added'.format(token_type.capitalize())}, 
                    status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
        except TokenICOKYCError as tik:
            return Response(tik.errors, 
                    status=status.HTTP_412_PRECONDITION_FAILED)
        except KeyError:
            return Response({'email': ["This field must not be blank"]}, 
                    status=status.HTTP_400_BAD_REQUEST)
                    

class UserRelationalViewSet(viewsets.ViewSet):
    serializer_class = UserRelationalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, APIUserPermission]

    @list_route(methods=['patch'])
    def start_project(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.exists():
            try:
                user = User.objects.get(email=serializer.data['email'])
                device = User.devices.get(uid=serializer.data['device_id'])
                device.start_project(url=serializer.data['url'])
                return Response({'success': "Project successfully started"}, 
                    status=status.HTTP_200_OK)
            except DeviceClientError as dce:
                return Response(dce.errors, 
                    status=status.HTTP_400_BAD_REQUEST)
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['patch'])
    def stop_project(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.exists():
            try:
                user = User.objects.get(email=serializer.data['email'])
                device = User.devices.get(uid=serializer.data['device_id'])
                device.stop_project(url=serializer.data['url'])

                return Response({'success': "Project successfully stopped"}, 
                    status=status.HTTP_200_OK)
            except DeviceClientError as dce:
                return Response(dce.errors, 
                    status=status.HTTP_400_BAD_REQUEST)
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




