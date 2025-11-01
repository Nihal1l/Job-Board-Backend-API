from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from employer.models import Job
from users.models import User

# Create your models here.
class SavedJob(models.Model):
    """Jobs saved by job seekers"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_seeker = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='saved_jobs'
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_by')

    class Meta:
        unique_together = ('job_seeker', 'job')
        verbose_name = _('Saved Job')
        verbose_name_plural = _('Saved Jobs')
        ordering = ['-id']
    
    def __str__(self):
        return f"{self.job_seeker.first_name} saved {self.job.title}"