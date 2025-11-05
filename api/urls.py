from django.urls import path, include
from users.views import *
from employer.views import *
from job_seeker.views import *
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('jobs', MyJobsViewSet, basename='job') 
router.register('appliedJobs', AppliedJobsListViewSet, basename='appliedJob') 
router.register('profile', ProfileView, basename='profile') 

job_router = routers.NestedDefaultRouter(
    router, 'jobs', lookup='job')
job_router.register('applys', AppliedJobsViewSet, basename='job-apply')
job_router.register('appliedCandidates', JobApplicantsViewSet, basename='appliedCandidate')

# profile_router = routers.NestedDefaultRouter(
#     router, 'profile', lookup='profile')
# profile_router.register('deleteResume', ProfileView, basename='deleteResume')



urlpatterns = [
    path('', include(router.urls)),
    path('', include(job_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]