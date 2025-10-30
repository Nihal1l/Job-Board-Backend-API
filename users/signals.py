"""
===========================================
apps/users/signals.py
===========================================
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, JobSeekerProfile, EmployerProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create profile when user is created"""
    if created:
        if instance.role == 'job_seeker' and not hasattr(instance, 'job_seeker_profile'):
            JobSeekerProfile.objects.create(user=instance)
        elif instance.role == 'employer' and not hasattr(instance, 'employer_profile'):
            EmployerProfile.objects.create(user=instance, company_name='')

