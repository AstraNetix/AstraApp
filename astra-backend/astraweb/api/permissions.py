from rest_framework import permissions

class APIUserPermission(permissions.BasePermission):
	"""
	Permission set for API calls from investor site
	"""
	def has_permission(self, request, view):
		# Only allows if api user
		return request.user.is_api_user	