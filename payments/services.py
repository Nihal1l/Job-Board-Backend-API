# ============================================
# STEP 5: Payment Service (payments/services.py)
# ============================================

import razorpay
import hmac
import hashlib
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import PaymentOrder, PaymentTransaction, UserSubscription, PremiumFeature


class RazorpayService:
    """Service class to handle Razorpay operations"""
    
    def __init__(self):
        self.client = razorpay.Client(auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        ))
    
    def create_order(self, user, feature_id):
        """Create a Razorpay order"""
        try:
            # Get feature
            feature = PremiumFeature.objects.get(id=feature_id, is_active=True)
            
            # Convert amount to paise (Razorpay expects amount in smallest currency unit)
            amount_paise = int(float(feature.price) * 100)
            
            # Generate unique receipt number
            receipt = f"rcpt_{user.id}_{timezone.now().timestamp()}"
            
            # Create Razorpay order
            razorpay_order = self.client.order.create({
                'amount': amount_paise,
                'currency': 'INR',
                'receipt': receipt,
                'notes': {
                    'user_id': user.id,
                    'feature_id': feature.id,
                    'feature_name': feature.name,
                }
            })
            
            # Save order in database
            payment_order = PaymentOrder.objects.create(
                user=user,
                premium_feature=feature,
                razorpay_order_id=razorpay_order['id'],
                amount=feature.price,
                currency='INR',
                receipt_number=receipt,
                status='created',
                notes=razorpay_order.get('notes', {})
            )
            
            return {
                'order_id': razorpay_order['id'],
                'amount': amount_paise,
                'currency': 'INR',
                'key_id': settings.RAZORPAY_KEY_ID,
                'name': feature.name,
                'description': feature.description,
                'prefill': {
                    'email': user.email,
                    'contact': getattr(user, 'phone', ''),
                }
            }
        
        except PremiumFeature.DoesNotExist:
            raise ValueError("Feature not found")
        except Exception as e:
            raise Exception(f"Error creating order: {str(e)}")
    
    def verify_payment(self, razorpay_order_id, razorpay_payment_id, razorpay_signature):
        """Verify payment signature"""
        try:
            # Get payment order
            payment_order = PaymentOrder.objects.get(razorpay_order_id=razorpay_order_id)
            
            # Verify signature
            generated_signature = hmac.new(
                settings.RAZORPAY_KEY_SECRET.encode('utf-8'),
                f"{razorpay_order_id}|{razorpay_payment_id}".encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            if generated_signature != razorpay_signature:
                payment_order.status = 'failed'
                payment_order.save()
                raise ValueError("Invalid payment signature")
            
            # Fetch payment details from Razorpay
            payment_details = self.client.payment.fetch(razorpay_payment_id)
            
            # Update payment order
            payment_order.razorpay_payment_id = razorpay_payment_id
            payment_order.razorpay_signature = razorpay_signature
            payment_order.status = 'paid'
            payment_order.paid_at = timezone.now()
            payment_order.save()
            
            # Create transaction record
            transaction = PaymentTransaction.objects.create(
                payment_order=payment_order,
                user=payment_order.user,
                transaction_id=razorpay_payment_id,
                amount=payment_order.amount,
                status=payment_details['status'],
                method=payment_details.get('method', ''),
                description=f"Payment for {payment_order.premium_feature.name}",
                metadata=payment_details
            )
            
            # Activate subscription
            self._activate_subscription(payment_order)
            
            return {
                'success': True,
                'message': 'Payment verified successfully',
                'payment_id': razorpay_payment_id,
                'order_id': razorpay_order_id
            }
        
        except PaymentOrder.DoesNotExist:
            raise ValueError("Order not found")
        except Exception as e:
            raise Exception(f"Error verifying payment: {str(e)}")
    
    def _activate_subscription(self, payment_order):
        """Activate user subscription after successful payment"""
        feature = payment_order.premium_feature
        start_date = timezone.now()
        
        # Calculate end date
        if feature.duration_days > 0:
            end_date = start_date + timedelta(days=feature.duration_days)
        else:
            # One-time purchase, set end date far in future
            end_date = start_date + timedelta(days=365*100)
        
        # Deactivate any existing active subscriptions for this feature
        UserSubscription.objects.filter(
            user=payment_order.user,
            premium_feature=feature,
            is_active=True
        ).update(is_active=False)
        
        # Create new subscription
        subscription = UserSubscription.objects.create(
            user=payment_order.user,
            premium_feature=feature,
            payment_order=payment_order,
            start_date=start_date,
            end_date=end_date,
            is_active=True
        )
        
        return subscription
    
    def get_payment_details(self, payment_id):
        """Fetch payment details from Razorpay"""
        try:
            return self.client.payment.fetch(payment_id)
        except Exception as e:
            raise Exception(f"Error fetching payment details: {str(e)}")
    
    def refund_payment(self, payment_id, amount=None):
        """Initiate refund for a payment"""
        try:
            refund_data = {'payment_id': payment_id}
            if amount:
                refund_data['amount'] = int(float(amount) * 100)
            
            refund = self.client.payment.refund(payment_id, refund_data)
            
            # Update payment order status
            PaymentOrder.objects.filter(
                razorpay_payment_id=payment_id
            ).update(status='refunded')
            
            return refund
        except Exception as e:
            raise Exception(f"Error processing refund: {str(e)}")