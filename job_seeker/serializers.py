from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model



class SimpleUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(
        method_name='get_current_user_name')

    class Meta:
        model = get_user_model()
        fields = ['id', 'name']

    def get_current_user_name(self, obj):
        return obj.get_username()


class AppliedJobsSerializer(serializers.ModelSerializer):
    # user = SimpleUserSerializer()
    user = serializers.SerializerMethodField(method_name='get_user')

    class Meta:
        model = appliedJobs
        fields = '__all__'
        read_only_fields = ['user', 'job', 'applied_at','status']

    def get_user(self, obj):
        return SimpleUserSerializer(obj.user).data

    def create(self, validated_data):
        job_id = self.context['job_id']
        return appliedJobs.objects.create(job_id=job_id, **validated_data)