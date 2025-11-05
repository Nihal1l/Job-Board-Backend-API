from django.shortcuts import render
from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .filters import JobCategoryFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import JobCategory, Job
from .serializers import JobCategorySerializer, JobSerializer, AppliedCandidatesSerializer
from job_seeker.serializers import AppliedJobsSerializer
from .permissions import IsEmployerOrReadOnly, IsEmployer
from job_seeker.models import *
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

class JobCategoryListView(generics.ListAPIView):
    """List all job categories"""
    
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer
    permission_classes = [IsEmployerOrReadOnly]



    

class JobApplicantsViewSet(ModelViewSet):
    serializer_class = AppliedCandidatesSerializer
    permission_classes = [IsEmployer]
    http_method_names = ['get', 'put', 'patch',  'head', 'options', 'trace']

    def get_queryset(self):
        return appliedJobs.objects.filter(job_id=self.kwargs.get('job_pk'))

    # def create(self, request, *args, **kwargs):
    #     """Only authenticated admin can create product"""
    #     return super().create(request, *args, **kwargs)
    
    def get_serializer_context(self):
        return {'job_id': self.kwargs.get('job_pk')}
    

class MyJobsViewSet(ModelViewSet):
    """List jobs posted by current employer"""
    
    serializer_class = JobSerializer
    permission_classes = [IsEmployerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = JobCategoryFilter
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        if not self.request.user.is_staff or self.request.user.is_anonymous or self.request.user.is_superuser:
            return Job.objects.all()
        else:
            return Job.objects.filter(user=self.request.user)




