from django.shortcuts import render
from rest_framework import status, permissions, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *

class ProfileView(ModelViewSet):
    """Get and update user profile"""
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'put', 'patch','delete']

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Deleting profiles is not allowed'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    @action(detail=False, methods=['get', 'put', 'patch'], url_path='edit_Profile')
    def edit_Profile(self, request):
        """Get or update current user's profile"""
        profile = request.user.profile
        
        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        
        # Handle PUT/PATCH
        partial = request.method == 'PATCH'
        serializer = self.get_serializer(profile, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='delete_Profile')
    def delete_resume(self, request):
        """Delete only the resume file, not the profile"""
        try:
            profile = request.user.profile
            
            if profile.resume:
                # Delete the file from storage
                profile.resume.delete(save=False)
                # Clear the field
                profile.resume = None
                profile.save()
                
                return Response(
                    {'message': 'Resume deleted successfully'},
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response(
                    {'error': 'No resume found to delete'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except Profile.DoesNotExist:
            return Response(
                {'error': 'Profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )


