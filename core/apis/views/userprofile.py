from core.models import UserProfile
from ..serializers.userprofile import UserProfileSerializer
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponseRedirect
from django.urls import reverse

class UserProfileViewSet(mixins.RetrieveModelMixin,mixins.ListModelMixin, GenericViewSet):
    serializer_class = UserProfileSerializer
    
    def get_queryset(self):
        return UserProfile.objects.select_related('user').all()
    
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
        profile = UserProfile.objects.get(user_id=request.user.id)
        was_following = profile.follow(pk)
        
        return Response({"message": "Followed successfully" if not was_following else "Already following"}, status=status.HTTP_200_OK)


    @action(detail=True, methods=['DELETE'], permission_classes=[IsAuthenticated])
    def unfollow(self, request, pk):
        profile = UserProfile.objects.get(user_id=request.user.id)
        was_following = profile.unfollow(pk)

        return Response({"message": "Unfollowed successfully" if was_following else "You are not following this user"}, status=status.HTTP_200_OK)


