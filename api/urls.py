from django.urls import path, include
from users.views import *
from employer.views import *
from job_seeker.views import *

from rest_framework_nested import routers

router = routers.DefaultRouter()
# router.register(r'users', UserViewSet, basename='user')
# router.register(r'profiles', ProfileViewSet, basename='profile')
router.register('my-jobs', MyJobsViewSet, basename='my-jobs') # employer_router = routers.NestedDefaultRouter(
#     router, 'employer', lookup='employer')

# urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    # path('employer/', include(employer_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]