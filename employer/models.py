from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.conf import settings

from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from employer.models import *
from users.models import User
from job_seeker.models import *


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
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL, 
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
    published_at = models.DateTimeField(auto_now_add=True, blank=True)
    
    class Meta:
        verbose_name = _('Job')
        verbose_name_plural = _('Jobs')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    






@receiver(post_save, sender=Job)
def notify_applicant_on_apply(sender, instance, created, **kwargs):
    if created:
        employer_email = instance.user.email
        job_title = instance.job.title
        
        try:
            send_mail(
                subject=f'New Applicant for : {job_title}',
                message=f'New Applicant for {job_title} at has been received successfully.',
                from_email=settings.DEFAULT_FROM_EMAIL,  # or 'noreply@yourjobboard.com'
                recipient_list=[employer_email],  # ✅ Must be a list!
                fail_silently=False,
            )
            print(f"✅ Email sent to {employer_email}")
        except Exception as e:
            print(f"❌ Failed to send email: {e}")           
    
