from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import PremiumFeature,  SelectedFeature
from .serializers import *
from employer.permissions import IsEmployer


class PremiumFeatureViewSet(viewsets.ModelViewSet):
    """ViewSet for browsing premium features"""
    
    serializer_class = PremiumFeatureSerializer
    permission_classes = [IsEmployer]
    http_method_names = ['get','head', 'options']
    
    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_anonymous or self.request.user.is_superuser:
            return PremiumFeature.objects.all()

class addFeatureViewSet(viewsets.ModelViewSet):
    """ViewSet for adding new premium features"""
    serializer_class = addFeatureSerializer
    permission_classes = [IsEmployer]
    http_method_names = ['post', 'get','head', 'options']
    
    def perform_create(self, serializer):
        serializer.save(purchaser=self.request.user)

    def perform_destroy(self, serializer):
        serializer.save(purchaser=self.request.user)

    def get_queryset(self):
        return SelectedFeature.objects.filter(feature_id=self.kwargs.get('feature_pk'))
     
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['feature_id'] = self.kwargs.get('feature_pk')
        return context

class SelectedFeatureViewSet(viewsets.ModelViewSet):
    """ViewSet for browsing selected features"""
    serializer_class = addFeatureSerializer
    permission_classes = [IsEmployer]
    http_method_names = ['get', 'delete']
        
    def get_queryset(self):
        return SelectedFeature.objects.filter(purchaser=self.request.user)
