"""
===========================================
apps/jobs/permissions.py
===========================================
"""

from rest_framework import permissions


class IsEmployerOrReadOnly(permissions.BasePermission):
    """Allow employers to create/edit, others to read"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff) 
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user or request.user.is_superuser
    
class IsEmployer(permissions.BasePermission):
    """Allow employers to create/edit, others to read"""
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff) 
    
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_staff)
  
    