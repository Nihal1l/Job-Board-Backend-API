from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings
import uuid 

User = get_user_model()

class PremiumFeature(models.Model):
    """Define available premium features"""

    id = models.BigAutoField(primary_key=True)


    FEATURE_TYPES = [
        ('featured_listing', 'Featured Job Listing'),
        ('advanced_tools', 'Advanced Recruitment Tools'),
        ('bulk_posting', 'Bulk Job Posting'),
        ('analytics', 'Advanced Analytics'),
    ]
    name = models.CharField(max_length=200, blank=True,default='null')
    feature_type = models.CharField(max_length=50, choices=FEATURE_TYPES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField(help_text="Duration in days (0 for one-time)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['price']
    
    def __str__(self):
        return f"{self.name} - ₹{self.price}"

class SelectedFeature(models.Model):
    """Model to retrieve a specific premium feature"""
    id = models.BigAutoField(primary_key=True)
    feature = models.ForeignKey(PremiumFeature, on_delete=models.CASCADE)
    purchaser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    
    class Meta:
        unique_together = ('feature', 'purchaser')

    def __str__(self):
        return f"Selected Feature: {self.feature.name}"
    

