from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import PremiumFeature, PaymentOrder, PaymentTransaction, UserSubscription
from .serializers import (
    PremiumFeatureSerializer, CreateOrderSerializer, PaymentVerificationSerializer,
    PaymentOrderSerializer, PaymentTransactionSerializer, UserSubscriptionSerializer
)
from .services import RazorpayService
from employer.permissions import IsEmployer



class PremiumFeatureViewSet(viewsets.ModelViewSet):
    """ViewSet for browsing premium features"""
    queryset = PremiumFeature.objects.filter(is_active=True)
    serializer_class = PremiumFeatureSerializer
    permission_classes = [IsEmployer]
    http_method_names = ['get', 'head', 'options']
    
    def get_queryset(self):
        return PremiumFeature.objects.filter(is_active=True).order_by('price')


class PaymentViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """ViewSet for handling payment operations"""
    permission_classes = [IsEmployer]
    serializer_class = PaymentOrderSerializer
    
    def get_queryset(self):
        """Get orders for specific feature if nested"""
        feature_pk = self.kwargs.get('feature_pk')
        if feature_pk:
            return PaymentOrder.objects.filter(
                user=self.request.user,
                premium_feature_id=feature_pk
            )
        return PaymentOrder.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Return appropriate serializer"""
        if self.action == 'create':
            return CreateOrderSerializer
        elif self.action == 'verify':
            return PaymentVerificationSerializer
        return PaymentOrderSerializer
    
    def create(self, request, *args, **kwargs):
        """Create payment order for a specific feature"""
        feature_pk = self.kwargs.get('feature_pk')
        
        # Override feature_id with the one from URL
        data = request.data.copy()
        if feature_pk:
            data['feature_id'] = feature_pk
        
        serializer = CreateOrderSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        try:
            razorpay_service = RazorpayService()
            order_data = razorpay_service.create_order(
                user=request.user,
                feature_id=serializer.validated_data['feature_id']
            )
            
            return Response({
                'success': True,
                'data': order_data
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def verify(self, request, feature_pk=None):
        """Verify payment"""
        serializer = PaymentVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            razorpay_service = RazorpayService()
            result = razorpay_service.verify_payment(
                razorpay_order_id=serializer.validated_data['razorpay_order_id'],
                razorpay_payment_id=serializer.validated_data['razorpay_payment_id'],
                razorpay_signature=serializer.validated_data['razorpay_signature']
            )
            
            return Response(result, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        

# payments/views.py (add this)

class PaymentManagementViewSet(viewsets.GenericViewSet):
    """Separate viewset for payment management operations"""
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentOrderSerializer
    
    @action(detail=False, methods=['post'], url_path='verify-payment')
    def verify_payment(self, request):
        """Verify payment signature"""
        serializer = PaymentVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            razorpay_service = RazorpayService()
            result = razorpay_service.verify_payment(
                razorpay_order_id=serializer.validated_data['razorpay_order_id'],
                razorpay_payment_id=serializer.validated_data['razorpay_payment_id'],
                razorpay_signature=serializer.validated_data['razorpay_signature']
            )
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='history')
    def payment_history(self, request):
        """Get user's payment history"""
        orders = PaymentOrder.objects.filter(user=request.user)
        serializer = PaymentOrderSerializer(orders, many=True)
        return Response({'success': True, 'data': serializer.data})
    
    @action(detail=False, methods=['get'], url_path='transactions')
    def transaction_history(self, request):
        """Get transaction history"""
        transactions = PaymentTransaction.objects.filter(user=request.user)
        serializer = PaymentTransactionSerializer(transactions, many=True)
        return Response({'success': True, 'data': serializer.data})
    
    @action(detail=False, methods=['get'], url_path='subscriptions')
    def active_subscriptions(self, request):
        """Get active subscriptions"""
        subscriptions = UserSubscription.objects.filter(
            user=request.user,
            is_active=True,
            end_date__gt=timezone.now()
        )
        serializer = UserSubscriptionSerializer(subscriptions, many=True)
        return Response({'success': True, 'data': serializer.data})
    
    """
```

**Final endpoints with hybrid approach:**
```
# Features
GET    /api/v1/features/                              # List features
GET    /api/v1/features/{id}/                         # Get feature detail

# Purchase (nested under features)
POST   /api/v1/features/{id}/purchases/               # Create order for feature
GET    /api/v1/features/{id}/purchases/               # List orders for feature

# Payment Management (separate)
POST   /api/v1/payments/verify-payment/               # Verify payment
GET    /api/v1/payments/history/                      # Payment history
GET    /api/v1/payments/transactions/                 # Transaction history
GET    /api/v1/payments/subscriptions/                # Active subscriptions

        
      

## Key Changes Made:

1. **Changed `PremiumFeatureViewSet`** from `ReadOnlyModelViewSet` to `ModelViewSet` with restricted HTTP methods
2. **Changed `PaymentViewSet`** from `ViewSet` to `GenericViewSet` - this provides the necessary base functionality
3. **Added `url_path` parameter** to all actions to create cleaner URLs with hyphens
4. **Added `get_serializer_class()`** method for proper serializer handling
5. **Removed `__init__`** method initialization of RazorpayService (create instance in each method instead)

## Updated API Endpoints:

With these changes, your endpoints will be:
```
GET    /api/v1/payments/features/                      # List all features
GET    /api/v1/payments/features/{id}/                 # Get specific feature

POST   /api/v1/payments/payments/create-order/        # Create payment order
POST   /api/v1/payments/payments/verify-payment/      # Verify payment
GET    /api/v1/payments/payments/payment-history/     # Get payment history
GET    /api/v1/payments/payments/transaction-history/ # Get transactions
GET    /api/v1/payments/payments/active-subscriptions/ # Get active subscriptions

"""