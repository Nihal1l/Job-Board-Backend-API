# ============================================
# STEP 7: URLs (payments/urls.py)
# ============================================

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PremiumFeatureViewSet, PaymentViewSet

router = DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
]