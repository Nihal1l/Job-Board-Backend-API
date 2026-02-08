from rest_framework import serializers
from .models import Order, PremiumFeature, FeatureItem, SelectedFeature

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class FeatureItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureItem
        fields = ['id', 'text']

class PremiumFeatureSerializer(serializers.ModelSerializer):
    items = FeatureItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = PremiumFeature
        fields = ['id', 'name', 'price', 'description', 'is_recommended', 'icon_type', 'items']

class SelectedFeatureSerializer(serializers.ModelSerializer):
    feature_name = serializers.CharField(source='feature.name', read_only=True)
    
    class Meta:
        model = SelectedFeature
        fields = ['id', 'user', 'feature', 'feature_name', 'order', 'purchased_at', 'is_active']
