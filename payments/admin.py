# ============================================
# STEP 8: Admin Configuration (payments/admin.py)
# ============================================

from django.contrib import admin
from .models import PremiumFeature, PaymentOrder, PaymentTransaction, UserSubscription


@admin.register(PremiumFeature)
class PremiumFeatureAdmin(admin.ModelAdmin):
    list_display = ['name', 'feature_type', 'price', 'duration_days', 'is_active', 'created_at']
    list_filter = ['feature_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']


@admin.register(PaymentOrder)
class PaymentOrderAdmin(admin.ModelAdmin):
    list_display = ['razorpay_order_id', 'user', 'amount', 'status', 'created_at', 'paid_at']
    list_filter = ['status', 'created_at', 'paid_at']
    search_fields = ['razorpay_order_id', 'razorpay_payment_id', 'user__email']
    readonly_fields = ['razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature']


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'user', 'amount', 'status', 'method', 'created_at']
    list_filter = ['status', 'method', 'created_at']
    search_fields = ['transaction_id', 'user__email']


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'premium_feature', 'start_date', 'end_date', 'is_active']
    list_filter = ['is_active', 'premium_feature', 'created_at']
    search_fields = ['user__email', 'premium_feature__name']