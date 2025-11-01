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
        return request.user.is_authenticated 
        # return request.user.is_authenticated and request.user.role == 'employer'
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.employer == request.user
    