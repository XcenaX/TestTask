from rest_framework import permissions
from django.conf import settings

class IsMainRole(permissions.BasePermission):
    def has_permission(self, request, view):
        user_roles = [role.name for role in request.user.roles.all()]
        return any(role in settings.MAIN_ROLES for role in user_roles)
