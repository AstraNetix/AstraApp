from rest_framework import permissions

class SuperUserPermission(permissions.BasePermission):
	"""
	Permission set for API calls from front end
	"""
	def has_permission(self, request, view):
		# Only allows if superuser
		return request.user.is_superuser	