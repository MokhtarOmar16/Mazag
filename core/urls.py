from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .apis.views import userprofile 

# إنشاء راوتر
router = DefaultRouter()
router.register(r'', userprofile.UserProfileViewSet, basename='user-profile')

urlpatterns = [
    path('', include(router.urls)),
]
