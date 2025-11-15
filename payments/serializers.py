# ============================================
# Serializers (payments/serializers.py)
# ============================================

from rest_framework import serializers
from .models import PremiumFeature, SelectedFeature
from job_seeker.serializers import SimpleUserSerializer

class PremiumFeatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = PremiumFeature
        fields = '__all__'
        read_only_fields = ['name', 'created_at']    

class addFeatureSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = SelectedFeature
        fields = ['id', 'feature', 'purchaser', 'user']
        read_only_fields = ['id', 'purchaser', 'user', 'feature']  # Make feature read-only
    
    def get_user(self, obj):
        return SimpleUserSerializer(obj.purchaser).data
    
    def create(self, validated_data):
        feature_id = self.context.get('feature_id')
        
        if not feature_id:
            raise serializers.ValidationError("Feature ID is required")
        
        # Get the purchaser from context
        purchaser = self.context['request'].user
        
        # Create the SelectedFeature with feature_id
        return SelectedFeature.objects.create(
            feature_id=feature_id,  # Use feature_id directly
            purchaser=purchaser
        )  

class SelectedFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectedFeature
        fields = ['id', 'feature', 'purchaser']
        # read_only_fields = ['id', 'feature', 'purchaser']



