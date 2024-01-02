# permissions.py

from rest_framework import permissions

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow unrestricted access for GET requests
        if request.method == 'GET':
            return True
        
        if request.user.is_superuser:
            return True
        
        return request.user.groups.filter(name='Manager').exists()


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    

class OnlyManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return request.user.groups.filter(name='Manager').exists()
    
class OrdersPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow unrestricted access for GET requests
        if request.method == 'GET':
            return True
        
        if request.user.is_superuser:
            return True
        
        if request.method == 'DELETE' and request.user.groups.filter(name='Manager').exists():
            return True 
        # Check if the user is in the "manager" group
        if request.method == 'POST' and not request.user.groups.filter(name='Manager').exists() or not request.user.groups.filter(name='Delivery-Crew').exists():
            return True
        
        if request.method == 'PATCH' and request.user.groups.filter(name='Delivery Crew').exists():
            return True
        
        if request.method == 'PUT' or 'PATCH'  and request.user.groups.filter(name='Manager').exists() or request.user.groups.filter(name='Delivery-Crew').exists():
            return False
        
        return False

