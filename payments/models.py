from django.db import models
from django.conf import settings
import uuid

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Ready To Ship', 'Ready To Ship'),
        ('Failed', 'Failed'),
        ('Cancelled', 'Cancelled'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} for {self.user.email}"


class PremiumFeature(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    is_recommended = models.BooleanField(default=False)
    icon_type = models.CharField(max_length=50, default='basic') # e.g., 'basic', 'pro', 'premium'

    def __str__(self):
        return self.name


class FeatureItem(models.Model):
    premium_feature = models.ForeignKey(PremiumFeature, on_delete=models.CASCADE, related_name='items')
    text = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.premium_feature.name} - {self.text}"


class SelectedFeature(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='selected_features')
    feature = models.ForeignKey(PremiumFeature, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True, blank=True)
    purchased_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.feature.name}"
