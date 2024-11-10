from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..serializers.follow import *
from ...pagination import CustomPagination 


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
    pagination_class = CustomPagination
    
    
    @action(detail=True, methods=['GET'])
    def followers(self, request, pk):
        target_user = User.objects.get(pk=pk)
        followers = target_user.user_followers.select_related("follower", "follower__profile").all()
        
        paginator = self.pagination_class()
        paginated_followers = paginator.paginate_queryset(followers, request)
        serializer = FollowersSerializer(paginated_followers, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(detail=True, methods=['GET'])
    def following(self, request, pk):
        target_user = User.objects.get(pk=pk)
        following = target_user.user_following.select_related("following", "following__profile").all()
            
        paginator = self.pagination_class()
        paginated_following = paginator.paginate_queryset(following, request)
        serializer = FollowingSerializer(paginated_following, many=True)
        return paginator.get_paginated_response(serializer.data)