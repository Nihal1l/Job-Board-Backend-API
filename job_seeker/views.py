from employer.models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from .permissions import IsApplicantAuthorOrReadonly
from drf_yasg.utils import swagger_auto_schema
from .models import appliedJobs
# Create your views here.


class AppliedJobsViewSet(ModelViewSet):
    serializer_class = AppliedJobsSerializer
    permission_classes = [IsApplicantAuthorOrReadonly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return appliedJobs.objects.filter(job_id=self.kwargs.get('job_pk'))

    def create(self, request, *args, **kwargs):
        """Only authenticated admin can create product"""
        return super().create(request, *args, **kwargs)
    
    def get_serializer_context(self):
        return {'job_id': self.kwargs.get('job_pk')}
    

class AppliedJobsListViewSet(ModelViewSet):
    serializer_class = AppliedJobsSerializer
    permission_classes = [IsApplicantAuthorOrReadonly]
    http_method_names = ['get', 'delete']

    def get_queryset(self):
        return appliedJobs.objects.filter(user=self.request.user)
