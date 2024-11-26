from django.urls import path
from .apis.views.user import UserMeViewSet,UserRegisterView, ChangePasswordView
from rest_framework.routers import DefaultRouter
from .apis.views import userprofile 
from .apis.views import follow 

router = DefaultRouter()
router.register('profiles', userprofile.ProfileViewSet, basename="profile")


urlpatterns = [
    
    path('users/me/', UserMeViewSet.as_view({'get': 'retrieve', 'patch': 'update', 'delete':'destroy'}), name="users-me"),
    path('users/', UserRegisterView.as_view(), name='user'), 
    path('users/changepassword/', ChangePasswordView.as_view(), name='user-changepassword'), 
    path('profiles/<int:pk>/follow/', follow.FollowViewSet.as_view({'post': 'follow', 'delete': 'unfollow'})),
    path('profiles/<int:pk>/followers/', follow.FollowersFollowingViewSet.as_view({'get': 'followers'})),
    path('profiles/<int:pk>/following/', follow.FollowersFollowingViewSet.as_view({'get': 'following'})),
    path('profiles/me/', userprofile.MeViewSet.as_view({'get': 'retrieve', 'patch': 'update'}), name="profile-me"),
] 


urlpatterns += router.urls