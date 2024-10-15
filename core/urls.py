from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .apis.views import userprofile 
from .apis.views import follow 

router = DefaultRouter()
router.register('profiles', userprofile.ProfileViewSet, basename="profile")


urlpatterns = [
    path('profiles/<int:pk>/follow/', follow.FollowViewSet.as_view({'post': 'follow', 'delete': 'unfollow'})),
    path('profiles/<int:pk>/followers/', follow.FollowersFollowingViewSet.as_view({'get': 'followers'})),
    path('profiles/<int:pk>/following/', follow.FollowersFollowingViewSet.as_view({'get': 'following'})),
    path('profiles/me/', userprofile.MeViewSet.as_view({'get': 'retrieve', 'patch': 'update'}), name="profile-me"),
]

urlpatterns += router.urls
