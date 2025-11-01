"""
===========================================
apps/jobs/serializers.py
===========================================
"""

from rest_framework import serializers
from .models import JobCategory, Job
from job_seeker.models import SavedJob


class JobCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = JobCategory
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    is_saved = serializers.SerializerMethodField()
    
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('employer','created_at', 'updated_at')
    
    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return SavedJob.objects.filter(job_seeker=request.user, job=obj).exists()
        return False


class JobListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for job listings"""
    
    company_name = serializers.CharField(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Job
        fields = (
            'id', 'title', 'company_name', 'category_name', 'job_type',
            'location','created_at'
        )


class SavedJobSerializer(serializers.ModelSerializer):
    job = JobListSerializer(read_only=True)
    
    class Meta:
        model = SavedJob
        fields = '__all__'
        read_only_fields = ('job_seeker', 'created_at')

