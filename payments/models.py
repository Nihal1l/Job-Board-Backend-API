from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class PremiumFeature(models.Model):
    """Define available premium features"""
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


class PaymentOrder(models.Model):
    """Store Razorpay order details"""
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('attempted', 'Attempted'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_orders')
    premium_feature = models.ForeignKey(PremiumFeature, on_delete=models.SET_NULL, null=True)
    
    # Razorpay fields
    razorpay_order_id = models.CharField(max_length=100, unique=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)
    
    # Payment details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='INR')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    
    # Metadata
    receipt_number = models.CharField(max_length=100, unique=True)
    notes = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.razorpay_order_id} - {self.user.email}"


class PaymentTransaction(models.Model):
    """Track all payment transactions and history"""
    payment_order = models.ForeignKey(PaymentOrder, on_delete=models.CASCADE, related_name='transactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    
    # Transaction details
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    method = models.CharField(max_length=50, blank=True)  # card, upi, netbanking, etc.
    
    # Additional info
    description = models.TextField(blank=True)
    error_message = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Transaction {self.transaction_id}"


class UserSubscription(models.Model):
    """Track user's active premium features"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    premium_feature = models.ForeignKey(PremiumFeature, on_delete=models.CASCADE)
    payment_order = models.ForeignKey(PaymentOrder, on_delete=models.SET_NULL, null=True)
    
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    auto_renew = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'premium_feature', 'is_active']
    
    def __str__(self):
        return f"{self.user.email} - {self.premium_feature.name}"
    
    def is_expired(self):
        return timezone.now() > self.end_date
