from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import *
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer



class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name')


class UserSerializer(BaseUserSerializer):
    class Meta:
        model = User
        ref_name = 'CustomUser'
        fields = ('id', 'email', 'first_name', 'last_name', 'is_staff')
        read_only_fields = ('is_staff',)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'resume', 'user')
        read_only_fields = ('user',)


class ResendActivationSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
            if user.is_active:
                raise serializers.ValidationError("This account is already active.")
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")

        



