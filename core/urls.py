from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .apis.views import userprofile 
from .apis.views import follow

router = DefaultRouter()
router.register('profile', userprofile.ProfileViewSet, basename="profile")

urlpatterns = [
    path('profile/<int:pk>/follow/', follow.FollowViewSet.as_view({'post': 'follow', 'delete': 'unfollow'})),
    path('profile/<int:pk>/followers/', follow.FollowersFollowingViewSet.as_view({'get': 'followers'})),
    path('profile/<int:pk>/following/', follow.FollowersFollowingViewSet.as_view({'get': 'following'})),
]

urlpatterns += router.urls
