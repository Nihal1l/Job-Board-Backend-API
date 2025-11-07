from django.urls import path, include
from users.views import *
from employer.views import *
from job_seeker.views import *
from payments.views import *
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register('jobs', MyJobsViewSet, basename='job') 
router.register('appliedJobs', AppliedJobsListViewSet, basename='appliedJob') 
router.register('profile', ProfileView, basename='profile') 
router.register('features', PremiumFeatureViewSet, basename='feature')

job_router = routers.NestedDefaultRouter(
    router, 'jobs', lookup='job')
job_router.register('applys', AppliedJobsViewSet, basename='job-apply')
job_router.register('appliedCandidates', JobApplicantsViewSet, basename='appliedCandidate')
job_router.register('reviews', ReviewViewSet, basename='job/Employer-review')


# Nested router for creating orders under features
feature_router = routers.NestedDefaultRouter(router, 'features', lookup='feature')
feature_router.register('purchases', PaymentViewSet, basename='purchase')

# Separate router for payment management endpoints
payment_router = DefaultRouter()
payment_router.register('payments', PaymentManagementViewSet, basename='payment-management')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(feature_router.urls)),
    path('', include(payment_router.urls)),
    path('', include(job_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]