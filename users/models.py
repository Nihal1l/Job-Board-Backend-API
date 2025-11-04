from django.contrib.auth.models import AbstractUser, BaseUserManager,  PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
import os
from dotenv import load_dotenv
from users.managers import CustomUserManager
load_dotenv()


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user using email instead of username."""
        if not email:
            raise ValueError("Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'        # ✅ Use email as username
    REQUIRED_FIELDS = []            # No username required

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# class User(AbstractUser):
#     """Custom User model with role-based access"""
    
#     ROLE_CHOICES = (
#         ('job_seeker', 'Job Seeker'),
#         ('employer', 'Employer'),
#         ('admin', 'Admin'),
#     )
    
#     username = None  # Remove username field
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     email = models.EmailField(_('email address'), unique=True)
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='job_seeker')
#     phone = models.CharField(max_length=20, blank=True, null=True)
#     email_verified = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name']
    
#     objects = UserManager()
    
#     class Meta:
#         verbose_name = _('user')
#         verbose_name_plural = _('users')
#         ordering = ['-created_at']
    
#     def __str__(self):
#         return self.email
    
#     @property
#     def full_name(self):
#         return f"{self.first_name} {self.last_name}".strip()


class EmailVerificationToken(models.Model):
    """Email verification token model"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verification_tokens')
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Token for {self.user.email}"


# class JobSeekerProfile(models.Model):
#     """Profile for job seekers"""
    
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='role')
#     bio = models.TextField(blank=True)
#     skills = models.TextField(blank=True, help_text="Comma-separated skills")
#     experience_years = models.IntegerField(default=0)
#     education = models.TextField(blank=True)
#     linkedin_url = models.URLField(blank=True, null=True)
#     github_url = models.URLField(blank=True, null=True)
#     portfolio_url = models.URLField(blank=True, null=True)
#     current_resume = models.FileField(upload_to='resumes/', blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         verbose_name = _('Job Seeker Profile')
#         verbose_name_plural = _('Job Seeker Profiles')
    
#     def __str__(self):
#         return f"{self.user.full_name}'s Profile"


# class EmployerProfile(models.Model):
#     """Profile for employers"""
    
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='role')
#     company_name = models.CharField(max_length=255)
#     company_description = models.TextField(blank=True)
#     company_website = models.URLField(blank=True, null=True)
#     company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
#     industry = models.CharField(max_length=100, blank=True)
#     company_size = models.CharField(max_length=50, blank=True)
#     location = models.CharField(max_length=255, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         verbose_name = _('Employer Profile')
#         verbose_name_plural = _('Employer Profiles')
    
#     def __str__(self):
#         return self.company_name


# class Resume(models.Model):
    # """Resume management for job seekers"""
    
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # job_seeker = models.ForeignKey(
    #     User, 
    #     on_delete=models.CASCADE, 
    #     related_name='resumes',
    #     limit_choices_to={'role': 'job_seeker'}
    # )
    # title = models.CharField(max_length=255)
    # file = models.FileField(upload_to='resumes/%Y/%m/')
    # is_default = models.BooleanField(default=False)
    # uploaded_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    
    # class Meta:
    #     ordering = ['-uploaded_at']
    #     verbose_name = _('Resume')
    #     verbose_name_plural = _('Resumes')
    
    # def __str__(self):
    #     return f"{self.title} - {self.job_seeker.full_name}"
    
    # def save(self, *args, **kwargs):
    #     if self.is_default:
    #         # Set all other resumes as non-default
    #         Resume.objects.filter(
    #             job_seeker=self.job_seeker, 
    #             is_default=True
    #         ).exclude(id=self.id).update(is_default=False)
    #     super().save(*args, **kwargs)