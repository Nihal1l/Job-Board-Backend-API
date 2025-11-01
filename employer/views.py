from django.shortcuts import render
from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import JobCategory, Job
from .serializers import JobCategorySerializer, JobSerializer, JobListSerializer, SavedJobSerializer
from .filters import JobFilter
from .permissions import IsEmployerOrReadOnly
from job_seeker.models import SavedJob
from rest_framework.viewsets import ModelViewSet
from api.permissions import IsAdminOrReadOnly

class JobCategoryListView(generics.ListAPIView):
    """List all job categories"""
    
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer
    permission_classes = [permissions.AllowAny]


class JobListCreateView(generics.ListCreateAPIView):
    """List and create jobs"""
    
    permission_classes = [IsEmployerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = JobFilter
    search_fields = ['title', 'description', 'requirements', 'location']
    ordering_fields = ['created_at']
    
    def get_queryset(self):
        return Job.objects.filter(status='published').select_related('employer', 'category')
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return JobListSerializer
        return JobSerializer
    
    def perform_create(self, serializer):
        job = serializer.save(
            employer=self.request.user,
        )
        
        if job.status == 'published':
            job.published_at = timezone.now()
            job.save()


class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, delete job"""
    
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsEmployerOrReadOnly]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def perform_update(self, serializer):
        job = serializer.save()
        
        if job.status == 'published' and not job.published_at:
            job.published_at = timezone.now()
            job.save()

class MyJobsViewSet(ModelViewSet):
    """List jobs posted by current employer"""
    
    serializer_class = JobSerializer
    permission_classes = [IsEmployerOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    
    def get_queryset(self):
        return Job.objects.filter(employer=self.request.user)


class SavedJobListView(generics.ListAPIView):
    """List saved jobs for job seeker"""
    
    serializer_class = SavedJobSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return SavedJob.objects.filter(job_seeker=self.request.user).select_related('job')


class SaveJobView(APIView):
    """Save or unsave a job"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        responses={200: 'Job saved/unsaved successfully'}
    )
    def post(self, request, pk):
        try:
            job = Job.objects.get(pk=pk, status='published')
        except Job.DoesNotExist:
            return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)
        
        saved_job, created = SavedJob.objects.get_or_create(
            job_seeker=request.user,
            job=job
        )
        
        if not created:
            saved_job.delete()
            return Response({'message': 'Job unsaved'}, status=status.HTTP_200_OK)
        
        return Response({'message': 'Job saved'}, status=status.HTTP_201_CREATED)



