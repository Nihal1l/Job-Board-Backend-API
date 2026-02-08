from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from django.http import HttpResponseRedirect
from .sslcommerz import SSLCOMMERZ
from django.conf import settings as main_settings
from .models import Order, PremiumFeature, SelectedFeature
from .serializers import OrderSerializer, PremiumFeatureSerializer, SelectedFeatureSerializer

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def initiate_payment(request):
    user = request.user
    # Accept frontend's actual field names
    plan_id = request.data.get("plan_id")
    amount = request.data.get("amount")
    
    if not all([plan_id, amount]):
        return Response({
            "status": "FAILED",
            "error": "Missing required fields",
            "required": ["plan_id", "amount"],
            "received": request.data
        }, status=status.HTTP_400_BAD_REQUEST)

    # Create an order for this payment
    if not user.is_authenticated:
        return Response({
            "error": "Authentication required",
            "message": "You must be logged in to initiate a payment. Please include your JWT token in the Authorization header.",
            "help": "Format: 'Authorization: JWT <your_token>'"
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        order = Order.objects.create(
            user=user,
            amount=amount,
            status='Pending'
        )
    except Exception as e:
        print(f"ERROR: Failed to create order: {str(e)}")
        print(f"ERROR: Exception type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return Response({
            "error": f"Failed to create order: {str(e)}",
            "exception_type": type(e).__name__
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    settings = {
        'store_id': 'dd6987a0bdee57a',
        'store_pass': 'dd6987a0bdee57a@ssl',
        'issandbox': True
    }
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = str(amount)
    post_body['currency'] = "BDT"
    post_body['tran_id'] = f"txn_{order.id}"
    post_body['success_url'] = f"{main_settings.BACKEND_URL}/api/v1/payment/success/"
    post_body['fail_url'] = f"{main_settings.BACKEND_URL}/api/v1/payment/fail/"
    post_body['cancel_url'] = f"{main_settings.BACKEND_URL}/api/v1/payment/cancel/"
    post_body['emi_option'] = 0
    
    # Handle potentially AnonymousUser
    if user.is_authenticated:
        post_body['cus_name'] = f"{user.first_name} {user.last_name}".strip() or "Guest User"
        post_body['cus_email'] = user.email or "guest@example.com"
        post_body['cus_phone'] = getattr(user, 'phone_number', '01700000000')
        post_body['cus_add1'] = getattr(user, 'address', 'Dhaka')
    else:
        post_body['cus_name'] = "Guest User"
        post_body['cus_email'] = "guest@example.com"
        post_body['cus_phone'] = "01700000000"
        post_body['cus_add1'] = "Dhaka"

    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "Courier"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "Premium Membership Plan"
    post_body['product_category'] = "Subscription"
    post_body['product_profile'] = "general"
    
    # Shipping information (required by SSLCommerz)
    post_body['ship_name'] = post_body['cus_name']
    post_body['ship_add1'] = post_body['cus_add1']
    post_body['ship_city'] = post_body['cus_city']
    post_body['ship_country'] = post_body['cus_country']
    post_body['ship_postcode'] = "1000"
    
    try:
        response = sslcz.createSession(post_body)  # API response
    except Exception as e:
        print(f"ERROR: SSLCommerz call failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({
            "error": "SSLCommerz API call failed",
            "details": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if response.get("status") == 'SUCCESS':
        return Response({"payment_url": response['GatewayPageURL']})
    return Response({
        "error": "Payment initiation failed",
        "details": response.get("failedreason", "Unknown error"),
        "response": response
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny]) # SSLCommerz calls this
def payment_success(request):
    print("Inside success")
    # SSLCommerz sends data in POST body
    tran_id = request.data.get("tran_id")
    if tran_id:
        try:
            # tran_id format is "txn_UUID"
            order_id = tran_id.split('_')[1]
            order = Order.objects.get(id=order_id)
            order.status = "Ready To Ship"
            order.save()
            
            # Activate the premium feature if linked
            SelectedFeature.objects.filter(order=order).update(is_active=True)
            
        except (Order.DoesNotExist, IndexError) as e:
            print(f"Error processing success callback: {e}")
            
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/?status=success&message=Payment%20Successful")


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def payment_cancel(request):
    print("Inside cancel")
    tran_id = request.data.get("tran_id")
    if tran_id:
        try:
            order_id = tran_id.split('_')[1]
            Order.objects.filter(id=order_id).update(status='Cancelled')
        except (Order.DoesNotExist, IndexError):
            pass
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/?status=cancel&message=Payment%20Cancelled")


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def payment_fail(request):
    print("Inside fail")
    tran_id = request.data.get("tran_id")
    if tran_id:
        try:
            order_id = tran_id.split('_')[1]
            Order.objects.filter(id=order_id).update(status='Failed')
        except (Order.DoesNotExist, IndexError):
            pass
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/?status=fail&message=Payment%20Failed")


# ViewSets for Plans
class PremiumFeatureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PremiumFeature.objects.all().prefetch_related('items')
    serializer_class = PremiumFeatureSerializer
    permission_classes = [permissions.AllowAny]

class addFeatureViewSet(viewsets.ModelViewSet):
    serializer_class = SelectedFeatureSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SelectedFeature.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        feature_id = self.kwargs.get('feature_pk') # From nested router
        try:
            feature = PremiumFeature.objects.get(id=feature_id)
        except PremiumFeature.DoesNotExist:
            return Response({"error": "Plan not found"}, status=status.HTTP_404_NOT_FOUND)

        # Create an Order
        order = Order.objects.create(
            user=request.user,
            amount=feature.price,
            status='Pending'
        )

        # Create/Update SelectedFeature
        selected_feature, created = SelectedFeature.objects.get_or_create(
            user=request.user,
            feature=feature,
            defaults={'order': order, 'is_active': False}
        )
        if not created:
            selected_feature.order = order
            selected_feature.save()

        return Response({
            "orderId": order.id,
            "amount": order.amount,
            "message": "Order created. Please initiate payment."
        }, status=status.HTTP_201_CREATED)

class SelectedFeatureViewSet(viewsets.ModelViewSet):
    serializer_class = SelectedFeatureSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SelectedFeature.objects.filter(user=self.request.user)
