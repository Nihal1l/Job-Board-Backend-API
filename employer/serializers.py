"""
===========================================
apps/jobs/serializers.py
===========================================
"""

from rest_framework import serializers
from .models import JobCategory, Job, Review
from job_seeker.models import appliedJobs
from django.contrib.auth import get_user_model

class SimpleUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(
        method_name='get_current_user_name')

    class Meta:
        model = get_user_model()
        fields = ['id', 'name']

    def get_current_user_name(self, obj):
        return obj.get_username()
    

class AppliedCandidatesSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name='get_user')
    
    class Meta:
        model = appliedJobs
        fields = '__all__'
        read_only_fields = ('job', 'applied_at', 'user', 'uploaded_resume', 'use_profile_resume')  
    
    def get_user(self, obj):
        return SimpleUserSerializer(obj.user).data
    
    def create(self, validated_data):
        job_id = self.context['job_id']
        user = self.context['request'].user  
        return appliedJobs.objects.create(
            job_id=job_id, 
            user=user,  
            **validated_data
        )


class JobCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = JobCategory
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    user = serializers.SerializerMethodField(method_name='get_user')
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('user','created_at', 'updated_at', 'published_at')

    def get_user(self, obj):
        return SimpleUserSerializer(obj.user).data    
    

class ReviewSerializer(serializers.ModelSerializer):
    # user = SimpleUserSerializer()
    user = serializers.SerializerMethodField(method_name='get_user')

    class Meta:
        model = Review
        fields = ['id', 'user', 'job', 'ratings', 'comment']
        read_only_fields = ['user', 'job']

    def get_user(self, obj):
        return SimpleUserSerializer(obj.user).data

    def create(self, validated_data):
        job_id = self.context['job_id']
        return Review.objects.create(job_id=job_id, **validated_data)


