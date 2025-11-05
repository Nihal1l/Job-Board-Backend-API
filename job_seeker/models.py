from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from employer.models import Job
from django.conf import settings
from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from employer.models import *
from users.models import *
from job_seeker.models import *



class appliedJobs(models.Model):
    """Jobs applied by job seekers"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='applied_jobs'
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    uploaded_resume = models.FileField(upload_to='resumes/', null=True, blank=True)  # Custom resume for this application
    use_profile_resume = models.BooleanField(default=False)  # Flag to use profile resume
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

    def get_resume(self):
        """Get the resume for this application"""
        if self.use_profile_resume and hasattr(self.user, 'profile'):
            return self.user.profile.resume
        return self.uploaded_resume    

    def __str__(self):
        return f"{self.user.email} applied for {self.job.title}"
    

@receiver(post_save, sender=appliedJobs)
def notify_applicant_on_apply(sender, instance, created, **kwargs):
    if created:
        applicant_email = instance.user.email
        job_title = instance.job.title
        company_name = instance.job.company.name if hasattr(instance.job, 'company') else 'the company'
        
        try:
            send_mail(
                subject=f'Application Confirmed: {job_title}',
                message=f'Your application for {job_title} at {company_name} has been submitted successfully.',
                from_email=settings.DEFAULT_FROM_EMAIL,  # or 'noreply@yourjobboard.com'
                recipient_list=[applicant_email],  # ✅ Must be a list!
                fail_silently=False,
            )
            print(f"✅ Email sent to {applicant_email}")
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
    