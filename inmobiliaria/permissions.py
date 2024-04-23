from rest_framework import permissions

class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Solo los superusuarios pueden acceder a este endpoint
        return request.user and request.user.is_superuser