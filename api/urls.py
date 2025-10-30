from django.urls import path, include
from users.views import *
from rest_framework_nested import routers

router = routers.DefaultRouter()
# urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]