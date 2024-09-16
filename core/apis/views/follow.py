from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..serializers.follow import *



User = get_user_model()


class FollowViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['POST'])
    def follow(self, request, pk=None):
        user = request.user
        target_user = User.objects.get(pk=pk)
        if user == target_user:
            return Response({"message": "You cannot follow yourself"}, status=status.HTTP_403_FORBIDDEN)

        if user.follow(target_user):
            return Response({"message": "You are now following this user"}, status=status.HTTP_200_OK)
        return Response({"message": "You are already following this user"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['DELETE'])
    def unfollow(self, request, pk=None):
        user = request.user
        target_user = User.objects.get(pk=pk)

        if user == target_user:
            return Response({"message": "You cannot unfollow yourself"}, status=status.HTTP_403_FORBIDDEN)

        if user.unfollow(target_user):
            return Response({"message": "You have unfollowed this user"}, status=status.HTTP_200_OK)
        return Response({"message": "You are not following this user"}, status=status.HTTP_400_BAD_REQUEST)


class FollowersFollowingViewSet(ViewSet):
    
    @action(detail=True, methods=['GET'])
    def followers(self, request, pk=None):
        target_user = User.objects.defer("is_staff", "is_active", "date_joined", "email").get(pk=pk)
        # followers = Follow.objects.filter(following=target_user).select_related('follower__profile','follower')
        followers = target_user.user_followers.\
            select_related("follower", "follower__profile")\
                .defer("follower__is_staff", "follower__is_active", "follower__date_joined", "follower__email").all()
        serializer = FollowersSerializer(followers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['GET'])
    def following(self, request, pk=None):
        target_user = User.objects.defer("is_staff", "is_active", "date_joined", "email").get(pk=pk)
        following = target_user.user_following.\
            select_related("following", "following__profile")\
                .defer("following__is_staff", "following__is_active", "following__date_joined", "following__email").all()
        serializer = FollowingSerializer(following, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)