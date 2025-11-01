from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

class JobCategory(models.Model):
    """Job categories/industries"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = _('Job Category')
        verbose_name_plural = _('Job Categories')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Job(models.Model):
    """Job listing model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employer = models.ForeignKey(
    User, 
    on_delete=models.CASCADE, 
    related_name='posted_jobs',
    null=True,  # Add this temporarily
    blank=True  # Add this temporarily
)
    category = models.ForeignKey(
        JobCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='jobs'
    )
    
    # Basic Information
    title = models.CharField(max_length=255)
    description = models.TextField()
    company_name = models.CharField(max_length=255)
    requirements = models.TextField()    
    location = models.CharField(max_length=255)    
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = _('Job')
        verbose_name_plural = _('Jobs')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    


# Your existing User model here...

class EmployerProfile(models.Model):
    """Profile for employers who post jobs"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='employer_profile'
    )
    company_name = models.CharField(max_length=255)
    company_description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.company_name} - {self.user.email}"

class JobSeekerProfile(models.Model):
    """Profile for job seekers"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='job_seeker_profile'
    )
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email}"
    


