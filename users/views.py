from django.shortcuts import render
from rest_framework import status, permissions, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *


# class RegisterView(APIView):
#     """User registration endpoint"""
    
#     permission_classes = [permissions.AllowAny]
    
#     @swagger_auto_schema(
#         request_body=UserCreateSerializer,
#         responses={201: UserSerializer(), 400: 'Bad Request'}
#     )
#     def post(self, request):
#         serializer = UserCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
            
#             # Create verification token
#             token = secrets.token_urlsafe(32)
#             EmailVerificationToken.objects.create(
#                 user=user,
#                 token=token,
#                 expires_at=timezone.now() + timedelta(hours=24)
#             )
            
#             # Send verification email
#             send_verification_email(user, token)
            
#             return Response({
#                 'message': 'Registration successful. Please check your email to verify your account.',
#                 'user': UserSerializer(user).data
#             }, status=status.HTTP_201_CREATED)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class VerifyEmailView(APIView):
#     """Email verification endpoint"""
    
#     permission_classes = [permissions.AllowAny]
    
#     @swagger_auto_schema(
#         manual_parameters=[
#             openapi.Parameter('token', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True)
#         ]
#     )
#     def get(self, request):
#         token = request.query_params.get('token')
        
#         try:
#             verification_token = EmailVerificationToken.objects.get(
#                 token=token,
#                 is_used=False,
#                 expires_at__gt=timezone.now()
#             )
            
#             user = verification_token.user
#             user.email_verified = True
#             user.is_active = True
#             user.save()
            
#             verification_token.is_used = True
#             verification_token.save()
            
#             return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
        
#         except EmailVerificationToken.DoesNotExist:
#             return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)


# class LoginView(APIView):
#     """User login endpoint"""
    
#     permission_classes = [permissions.AllowAny]
    
#     @swagger_auto_schema(
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 'email': openapi.Schema(type=openapi.TYPE_STRING),
#                 'password': openapi.Schema(type=openapi.TYPE_STRING),
#             }
#         ),
#         responses={200: 'Login successful'}
#     )
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
        
#         user = authenticate(email=email, password=password)
        
#         if user:
#             if not user.email_verified:
#                 return Response({
#                     'error': 'Email not verified. Please check your email for verification link.'
#                 }, status=status.HTTP_403_FORBIDDEN)
            
#             refresh = RefreshToken.for_user(user)
            
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#                 'user': UserSerializer(user).data
#             }, status=status.HTTP_200_OK)
        
#         return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



class ProfileView(ModelViewSet):
    """Get and update user profile"""
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'put', 'patch','delete']

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Deleting profiles is not allowed'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    @action(detail=False, methods=['get', 'put', 'patch'], url_path='edit_Profile')
    def edit_Profile(self, request):
        """Get or update current user's profile"""
        profile = request.user.profile
        
        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        
        # Handle PUT/PATCH
        partial = request.method == 'PATCH'
        serializer = self.get_serializer(profile, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(detail=False, methods=['delete'], url_path='delete_Profile')
    def delete_resume(self, request):
        """Delete only the resume file, not the profile"""
        try:
            profile = request.user.profile
            
            if profile.resume:
                # Delete the file from storage
                profile.resume.delete(save=False)
                # Clear the field
                profile.resume = None
                profile.save()
                
                return Response(
                    {'message': 'Resume deleted successfully'},
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response(
                    {'error': 'No resume found to delete'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except Profile.DoesNotExist:
            return Response(
                {'error': 'Profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )


