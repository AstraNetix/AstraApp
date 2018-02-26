from settings import AUTH_USER_MODEL as User
from api.models.device import Device
from api.serializers.user import (
	UserLoginSerializer, 
	UserPasswordResetSerializer,
	UserBasicSerializer, 
	UserICOKYCSerializer, 
	UserBalanceSerializer
	)
from api.permissions import SuperUserPermission

from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets

from rest_framework.decorators import detail_route, list_route	
from rest_framework.response import Response


class UserBasicViewSet(viewsets.ModelViewSet):
	serializer_class = UserBasicSerializer
	serializer_login_class = UserLoginSerializer
	serializer_password_class = UserPasswordResetSerializer
	queryset = User.objects.all()
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserPermission]

	@detail_route(methods=['patch'])
	def login_user(self, request, pk=None):
		serializer = self.serializer_login_class(data=request.data)
		
		if serializer.is_valid():
			try:
				user = User.authenticate(serializer.email, serializer.password)
				login(request, user)
			except AuthenticationError:
				return Response({'failure': "User failed to authenticate"}, 
					status=status.HTTP_401_UNAUTHORIZED)
		else: 
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@detail_route(methods=['patch'])		
	def logout_user(self, request, pk=None):
		logout(request)

	@detail_route(methods=['get'])
	def request_password_reset(self, request, pk=None):
		serializer = self.serializer_class(data=request.data)

		if serializer.is_valid():
			user = User.objects.get(email=serializer.email)
			user.reset_password_email()
		else: 
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@detail_route(methods=['get'])
	def reset_password(self, request, pk=None):
		serializer = self.serializer_password_class(data=request.data)

		if serializer.is_valid():
			user = User.objects.get(email=serializer.email)
			user.reset_password_email()
		else: 
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@detail_route(methods=['patch'])
	def set_user_verified(self, request, pk=None):
		serializer = self.serializer_class(data=request.data)

		if serializer.is_valid():
			user = self.get_object()
			user.set_email_valid()
			return Response({'success': "User successfully verified"}, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserICOKYCViewSet(viewsets.ModelViewSet):
	serializer_class = UserICOKYCSerializer
	queryset = User.objects.all()
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserPermission]

	@detail_route(methods=['get'])
	def user_valid_for_sale(self, request, pk=None):
		serializer = self.serializer_class(data=request.data)

		if serializer.is_valid():
			user = self.get_object()
			return Response(user.token_auth(), status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserBalanceViewSet(viewsets.ModelViewSet):
	serializer_class = UserBalanceSerializer
	queryset = User.objects.all()
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserPermission]

	@detail_route(methods=['patch'])
	def add_star(self, request, pk=None):
		return add_tokens(User.add_star_tokens)

	@detail_route(methods=['patch'])
	def add_usd(self, request, pk=None):
		return add_tokens(User.add_usd)

	@detail_route(methods=['patch'])
	def add_btc(self, request, pk=None):
		return add_tokens(User.add_bitcoin)

	@detail_route(methods=['patch'])
	def add_ether(self, request, pk=None):
		return add_tokens(User.add_ether)

	def add_tokens(func, token_type):
		user = self.get_object()
		serializer = self.serializer_class(data=request.data)

		if serializer.is_valid():
			try: 
				func(user, serializer.data[token_type])	
				return Response({'status': '{0} added'.format(token_type)})
			except TokenICOKYCError as tik:
				return Response({'status': str(tik)}, 
					status=status.HTTP_412_PRECONDITION_FAILED)
		else:
			return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)



