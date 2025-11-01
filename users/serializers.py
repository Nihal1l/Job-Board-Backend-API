from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer

# class UserCreateSerializer(serializers.ModelSerializer):
#     """Serializer for user registration"""
    
#     password = serializers.CharField(write_only=True, validators=[validate_password])
#     password_confirm = serializers.CharField(write_only=True)
    
#     class Meta:
#         model = User
#         fields = ('email', 'password', 'password_confirm', 'first_name', 'last_name', 'role', 'phone')
    
#     def validate(self, attrs):
#         if attrs['password'] != attrs['password_confirm']:
#             raise serializers.ValidationError({"password": "Passwords do not match"})
#         return attrs
    
#     def create(self, validated_data):
#         validated_data.pop('password_confirm')
#         user = User.objects.create_user(**validated_data)
        
#         # Create profile based on role
#         if user.role == 'job_seeker':
#             JobSeekerProfile.objects.create(user=user)
#         elif user.role == 'employer':
#             EmployerProfile.objects.create(user=user, company_name='')
        
#         return user

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ('id', 'email', 'password', 'first_name', 'last_name')
        


# class UserSerializer(serializers.ModelSerializer):
#     """Serializer for user details"""
    
#     job_seeker_profile = JobSeekerProfileSerializer(read_only=True)
#     employer_profile = EmployerProfileSerializer(read_only=True)
    
#     class Meta:
#         model = User
#         fields = (
#             'id', 'email', 'first_name', 'last_name', 'role', 'phone',
#             'email_verified', 'created_at', 'job_seeker_profile', 'employer_profile'
#         )
#         read_only_fields = ('id', 'email_verified', 'created_at')

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        ref_name = 'CustomUser'
        fields = ('id', 'email', 'first_name', 'last_name')
        
# class ResumeSerializer(serializers.ModelSerializer):
#     """Serializer for resume"""
    
#     class Meta:
#         model = Resume
#         fields = '__all__'
#         read_only_fields = ('job_seeker', 'uploaded_at', 'updated_at')

# class JobSeekerProfileSerializer(serializers.ModelSerializer):
#     """Serializer for job seeker profile"""
    
#     class Meta:
#         model = JobSeekerProfile
#         fields = '__all__'
#         read_only_fields = ('user', 'created_at', 'updated_at')


# class EmployerProfileSerializer(serializers.ModelSerializer):
#     """Serializer for employer profile"""
    
#     class Meta:
#         model = EmployerProfile
#         fields = '__all__'
#         read_only_fields = ('user', 'created_at', 'updated_at')


