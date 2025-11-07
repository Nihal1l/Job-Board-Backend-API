# ============================================
# STEP 4: Serializers (payments/serializers.py)
# ============================================

from rest_framework import serializers
from .models import PremiumFeature, PaymentOrder, PaymentTransaction, UserSubscription
from employer.serializers import SimpleUserSerializer


class PremiumFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PremiumFeature
        fields = ['id', 'name', 'feature_type', 'description', 'price', 
                  'duration_days', 'is_active', 'created_at']
        read_only_fields = ['id', 'name', 'created_at']

    # def get_user(self, obj):
    #     return SimpleUserSerializer(obj.user).data
class CreateOrderSerializer(serializers.Serializer):
    feature_id = serializers.IntegerField()
    
    def validate_feature_id(self, value):
        try:
            feature = PremiumFeature.objects.get(id=value, is_active=True)
            return value
        except PremiumFeature.DoesNotExist:
            raise serializers.ValidationError("Invalid or inactive feature")


class PaymentVerificationSerializer(serializers.Serializer):
    razorpay_order_id = serializers.CharField(max_length=100)
    razorpay_payment_id = serializers.CharField(max_length=100)
    razorpay_signature = serializers.CharField(max_length=200)


class PaymentOrderSerializer(serializers.ModelSerializer):
    premium_feature_name = serializers.CharField(source='premium_feature.name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = PaymentOrder
        fields = ['id', 'razorpay_order_id', 'amount', 'currency', 'status',
                  'receipt_number', 'premium_feature_name', 'user_email',
                  'created_at', 'paid_at']
        read_only_fields = fields


class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = ['id', 'transaction_id', 'amount', 'status', 'method',
                  'description', 'created_at']
        read_only_fields = fields


class UserSubscriptionSerializer(serializers.ModelSerializer):
    feature_name = serializers.CharField(source='premium_feature.name', read_only=True)
    feature_type = serializers.CharField(source='premium_feature.feature_type', read_only=True)
    is_expired = serializers.SerializerMethodField()
    
    class Meta:
        model = UserSubscription
        fields = ['id', 'feature_name', 'feature_type', 'start_date', 
                  'end_date', 'is_active', 'is_expired', 'created_at']
        read_only_fields = fields
    
    def get_is_expired(self, obj):
        return obj.is_expired()

