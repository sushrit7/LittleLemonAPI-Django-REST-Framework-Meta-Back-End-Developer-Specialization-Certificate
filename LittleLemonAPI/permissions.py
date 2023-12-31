# permissions.py

from rest_framework import permissions

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow unrestricted access for GET requests
        if request.method == 'GET':
            return True
        
        # Check if the user is in the "manager" group
        return request.user.groups.filter(name='Manager').exists()


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user