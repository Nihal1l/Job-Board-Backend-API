from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from employer.models import Job
from django.conf import settings

class appliedJobs(models.Model):
    """Jobs applied by job seekers"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='applied_jobs'
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    uploaded_resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('applied', 'Applied'),
            ('under_review', 'Under Review'),
            ('interview_scheduled', 'Interview Scheduled'),
            ('offered', 'Offered'),
            ('rejected', 'Rejected'),
        ],
        default='applied',
    )

    class Meta:
        unique_together = ('user', 'job')
        verbose_name = 'Applied Job'
        verbose_name_plural = 'Applied Jobs'
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.user.email} applied for {self.job.title}"
    

    