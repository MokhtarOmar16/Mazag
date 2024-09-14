from core.models import UserProfile
from ..serializers.userprofile import UserProfileSerializer, SimpleUserProfileSerializer
from ..serializers.follow import FollowersSerializer, FollowingSerializer
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class UserProfileViewSet(mixins.RetrieveModelMixin,mixins.ListModelMixin, GenericViewSet):
    queryset= UserProfile.objects.select_related('user').prefetch_related('follower','following').all()
    
    
    def get_serializer_class(self):
        if self.action == 'list':
            return SimpleUserProfileSerializer 
        return UserProfileSerializer  
    
    
    def get_serializer_context(self):
        return {"request":self.request}

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        profile = UserProfile.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer =UserProfileSerializer(profile)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = UserProfileSerializer(profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def follow(self, request, pk):
        profile_id_follower =request.user.data.id
        if str(pk) == str(profile_id_follower):
            return Response({"message":"you can not follow yourself"},status=status.HTTP_403_FORBIDDEN)
        
        profile = self.get_object()
        done = profile.follow(profile_id_follower)
        if not done:
            return Response({"message":"you already following this user"},status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(detail=True, methods=['DELETE'], permission_classes=[IsAuthenticated])
    def unfollow(self, request, pk):
        profile_id_follower =request.user.data.id
        if str(pk) == str(profile_id_follower):
            return Response({"message":"you can not un follow yourself"},status=status.HTTP_403_FORBIDDEN)
        
        profile = self.get_object()
        done = profile.unfollow(profile_id_follower)
        if not done:
            return Response({"message":"you already not following this user"},status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_204_NO_CONTENT)


    # @action(detail=True, methods=['GET'],permission_classes=[AllowAny])
    # def followers(self, request, pk):
    #     profile = self.get_object()
    #     followers = profile.followers.all()
    #     serializer = SimpleUserProfileSerializer(followers, many=1)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
        
    
    @action(detail=True, methods=['GET'],permission_classes=[AllowAny])
    def followers(self, request, pk):
        profile = self.get_object()
        followers = profile.follower.all()
        serializer = FollowersSerializer(followers, many=1)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['GET'],permission_classes=[AllowAny])
    def following(self, request, pk):
        profile = self.get_object()
        following = profile.following.all()
        serializer = FollowingSerializer(following, many=1)
        return Response(serializer.data, status=status.HTTP_200_OK)
        